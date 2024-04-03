from collections import defaultdict
from pathlib import Path
from dataclasses import asdict
import logging

from addict import Dict
from gregor_anvil_automation.utils.mappings import REFERENCE_SOURCE

from gregor_anvil_automation.utils.utils import get_table_samples
from ..utils.types import Sample, Table
from ..utils.issue import Issue
from ..utils.utils import generate_file, parse_file
from ..utils.email import send_email, ATTACHED_ISSUES_MSG_BODY, SUCCESS_MSG_BODY
from ..validation.schema import get_schema
from ..validation.sample import SampleValidator
from ..validation.checks import check_cross_references, check_uniqueness
from ..utils.mappings import HEADER_CASE_SENSITIVE_MAP


logger = logging.getLogger(__name__)


def run(
    config: Dict,
    input_path: Path,
    batch_number: str,
    working_dir: Path,
    metadata_map_file: Path,
) -> int:
    """The short_reads entry point"""
    tables = get_table_samples(input_path)
    issues = []
    apply_metadata_map_file(metadata_map_file, tables, config.gcp_bucket_name, issues)
    # Validate files
    validate_tables(
        batch_number=batch_number,
        issues=issues,
        tables=tables,
    )
    # If any errors, email issues in a csv file
    subject = "GREGoR AnVIL automation"
    if issues:
        file_path = working_dir / "issues.csv"
        data_headers = ["field", "message", "table_name", "row"]
        generate_file(file_path, data_headers, [asdict(issue) for issue in issues], ",")
        send_email(config["email"], subject, ATTACHED_ISSUES_MSG_BODY, [file_path])
        return 1
    file_paths = []
    for table_name, table in tables.items():
        if table_name in HEADER_CASE_SENSITIVE_MAP:
            for sample in table:
                for old_header, new_header in HEADER_CASE_SENSITIVE_MAP[
                    table_name
                ].items():
                    if old_header in sample:
                        sample[new_header] = sample.pop(old_header)
        # If all ok, generate tsvs of each table
        file_path = working_dir / f"{table_name}.tsv"
        data_headers = list(table[0].keys())
        data_headers.remove("row_number")
        generate_file(file_path, data_headers, table, "\t")
        file_paths.append(file_path)
    send_email(config["email"], subject, SUCCESS_MSG_BODY, file_paths)
    return 0


def apply_metadata_map_file(
    metadata_map_file: Path,
    tables: dict[str, list[Sample]],
    gcp_bucket_name: Path,
    issues: list[Issue],
):
    """Fills purposefully blank cells in specific tables with data from the metadata_map_file path"""
    metadata = parse_file(metadata_map_file, ",")

    base_gcp_path = f"gs://{gcp_bucket_name}"

    for line in metadata:
        md_algn_dna_id = line["aligned_dna_short_read_id"]
        md_expr_dna_id = line["experiment_dna_short_read_id"]
        algn_id_match = (
            False  # Specifies if at least one aligned_dna_short_read_id match was made
        )
        for sample in tables["aligned_dna_short_read"]:
            if (
                md_algn_dna_id == sample["aligned_dna_short_read_id"]
                and md_expr_dna_id == sample["experiment_dna_short_read_id"]
            ):
                algn_id_match = True
                if sample["aligned_dna_short_read_file"] == "NA":
                    cram_file_name = line["cram_file_name"]
                    sample[
                        "aligned_dna_short_read_file"
                    ] = f"{base_gcp_path}/{cram_file_name}"
                else:
                    sample_index = tables["aligned_dna_short_read"].index(sample)
                    logger.warning(
                        "Metadata Map File: Sample with aligned_dna_short_read_id %s at row %d has an aligned_dna_short_read_file that already exists",
                        md_algn_dna_id,
                        sample_index,
                    )
                if sample["aligned_dna_short_read_index_file"] == "NA":
                    crai_file_name = line["crai_file_name"]
                    sample[
                        "aligned_dna_short_read_index_file"
                    ] = f"{base_gcp_path}/{crai_file_name}"
                else:
                    sample_index = tables["aligned_dna_short_read"].index(sample)
                    logger.warning(
                        "Metadata Map File: Sample with aligned_dna_short_read_id %s at row %d has an aligned_dna_short_read_index_file that already exists",
                        md_algn_dna_id,
                        sample_index,
                    )
                if sample["md5sum"] == "NA":
                    sample["md5sum"] = line["md5sum"]
                else:
                    sample_index = tables["aligned_dna_short_read"].index(sample)
                    logger.warning(
                        "Metadata Map File: Sample with aligned_dna_short_read_id %s at row %d has an md5sum that already exists",
                        md_algn_dna_id,
                        sample_index,
                    )
        if not algn_id_match:
            field = (
                ["aligned_dna_short_read_id","experiment_dna_short_read_id"]
            )
            new_issue = Issue(
                field,
                f"Value {field} does not exist",
                "aligned_dna_short_read",
                None,
            )
            issues.append(new_issue)
            logger.error(
                "Metadata Map File: Value %s does not exist in table aligned_dna_short_read",
                field,
            )
        exp_id_match = False  # Specifies if at least one experiment_dna_short_read_id match was made
        for sample in tables["experiment_dna_short_read"]:
            if md_expr_dna_id == sample["experiment_dna_short_read_id"]:
                exp_id_match = True
                if sample["experiment_sample_id"] == "NA":
                    sample["experiment_sample_id"] = line["sm_tag"]
                else:
                    sample_index = tables["experiment_dna_short_read"].index(sample)
                    logger.warning(
                        "Metadata Map File: Sample with experiment_dna_short_read_id %s at row %d has an experiment_sample_id that already exists",
                        md_expr_dna_id,
                        sample_index,
                    )
        if not exp_id_match:
            field = "experiment_dna_short_read_id"
            new_issue = Issue(
                field,
                f"Value {field} does not exist",
                "experiment_dna_short_read",
                None,
            )
            issues.append(new_issue)
            logger.error(
                "Metadata Map File: Value %s does not exist in table experiment_dna_short_read",
                field,
            )


def validate_tables(batch_number: str, issues: list[Issue], tables: list[Table]):
    """Validates tables via normalization and checking uniqueness of values across tables"""
    ids = defaultdict(set)
    for table_name, samples in tables.items():
        # Validate sample by sample using cerberus
        samples = normalize_and_validate_samples(
            batch_number=batch_number,
            issues=issues,
            samples=samples,
            table_name=table_name,
        )
        # Validate Table Wide Issues which as of now is just unique checking
        check_uniqueness(samples, table_name, issues)
        if table_name in REFERENCE_SOURCE:
            ids[REFERENCE_SOURCE[table_name]].update(
                sample[REFERENCE_SOURCE[table_name]] for sample in samples
            )
        tables[table_name] = samples
    # Cross Reference Checks
    check_cross_references(ids, tables, issues)


def normalize_and_validate_samples(
    batch_number: str,
    issues: list[dict],
    samples: list[Sample],
    table_name: str,
):
    """Normalizes and validate samples"""
    schema = get_schema(table_name)
    sample_validator = SampleValidator(
        schema=schema,
        batch_number=batch_number,
    )
    sample_validator.allow_unknown = True
    normalized_samples = []
    for sample in samples:
        sample_validator.validate(sample)
        normalized_samples.append(sample_validator.document)
        issues.extend(
            convert_errors_to_issues(
                errors=sample_validator.errors,
                table_name=table_name,
                row=sample["row_number"],
            )
        )
    return normalized_samples


def convert_errors_to_issues(errors: list[dict], **kwargs) -> list[dict[str, str]]:
    """Convers from Cerberus errors to a dictionary of issues. We use the
    biobank_id, lims_id, and sample_id since a manifest is guaranteed to have
    at least one of these fields."""
    issues = []
    for field, messages in errors.items():
        for message in messages:
            issue = Issue(
                **kwargs,
                field=field,
                message=message,
            )
            issues.append(issue)
    return issues
