from collections import defaultdict
from pathlib import Path
from dataclasses import asdict
import logging
import datetime

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

    table_formats = {
        "aligned_dna_short_read": {
            "aligned_dna_short_read_id": "aligned_dna_short_read_id",
            "experiment_dna_short_read_id": "experiment_dna_short_read_id",
            "aligned_dna_short_read_file": "cram_file_name",
            "aligned_dna_short_read_index_file": "crai_file_name",
            "md5sum": "md5sum",
        },
        "experiment_dna_short_read": {
            "experiment_dna_short_read_id": "experiment_dna_short_read_id",
            "experiment_sample_id": "sm_tag",
        },
    }

    for line in metadata:
        for table_name, table_format in table_formats.items():
            for sample in tables[table_name]:
                id_match = False
                algn_match = True
                for table_field, metadata_field in table_format.items():
                    metadata_value = line[metadata_field]
                    cram_file_name = (
                        f"{base_gcp_path}/{metadata_value}.cram"
                        if metadata_field == "cram_file_name"
                        else None
                    )
                    crai_file_name = (
                        f"{base_gcp_path}/{metadata_value}.cram.crai"
                        if metadata_field == "crai_file_name"
                        else None
                    )
                    if (
                        sample[table_field] == "NA"
                        and table_field != "experiment_dna_short_read_id"
                        and table_field != "aligned_dna_short_read_id"
                    ):
                        if cram_file_name or crai_file_name:
                            sample[table_field] = (
                                cram_file_name if cram_file_name else crai_file_name
                            )
                        else:
                            sample[table_field] = metadata_value
                    elif sample[table_field] != metadata_value:
                        if not cram_file_name and not crai_file_name:
                            message = (
                                f"Metadata Map File Population: In table {table_name} on row {sample_idx} value {table_field} exists and does not match the Metadata Map File.",
                            )
                        sample_idx = sample["row_number"]
                        if table_field == "aligned_dna_short_read_id":
                            algn_match = False
                            if (
                                sample_idx == len(tables[table_name]) - 1
                                and not id_match
                            ):
                                message = f"Metadata Map File Population: In table {table_name} value {table_field} matches no {table_field} in the Metadata Map File."
                                sample_idx = None
                        new_issue = Issue(
                            table_field,
                            message,
                            table_name,
                            sample_idx,
                        )
                        issues.append(new_issue)
                        logger.error(message)
                        if table_field == "experiment_dna_short_read_id" and algn_match:
                            id_match = False


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
