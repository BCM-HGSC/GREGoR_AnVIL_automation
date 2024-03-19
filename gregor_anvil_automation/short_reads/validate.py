from collections import defaultdict
from pathlib import Path
from dataclasses import asdict

from addict import Dict
from gregor_anvil_automation.utils.mappings import REFERENCE_SOURCE

from gregor_anvil_automation.utils.utils import get_table_samples
from ..utils.types import Sample, Table
from ..utils.issue import Issue
from ..utils.utils import generate_file
from ..utils.email import send_email, ATTACHED_ISSUES_MSG_BODY, SUCCESS_MSG_BODY
from ..validation.schema import get_schema
from ..validation.sample import SampleValidator
from ..validation.checks import check_cross_references, check_uniqueness


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
    # Validate files
    validate_tables(
        batch_number=batch_number,
        gcp_bucket_name=config.gcp_bucket_name,
        issues=issues,
        tables=tables,
    )
    apply_metadata_map_file(metadata_map_file, tables, config.gcp_bucket_name)
    # If any errors, email issues in a csv file
    subject = "GREGoR AnVIL automation"
    if issues:
        file_path = working_dir / "issues.csv"
        data_headers = ["field", "message", "table_name", "row"]
        generate_file(file_path, data_headers, [asdict(issue) for issue in issues], ",")
        send_email(config, subject, ATTACHED_ISSUES_MSG_BODY, [file_path])
    # If all is good, email of success and files generated
    else:
        file_paths = []
        for table_name, table in tables.items():
            # If all ok, generate tsvs of each table
            file_path = working_dir / f"{table_name}.tsv"
            data_headers = table[0].keys()
            generate_file(file_path, data_headers, table, "\t")
            file_paths.append(file_path)
        send_email(config, subject, SUCCESS_MSG_BODY, file_paths)
    return 0


def apply_metadata_map_file(
    metadata_map_file: Path, tables: dict[str, list[Sample]], gcp_bucket_name: Path
):
    """Fills purposefully blank cells in specific tables with data from the metadata_map_file path"""
    metadata = get_table_samples(metadata_map_file)[0]
    aligned_dna_short_read_files_path_header = f"gs://{gcp_bucket_name}"

    # Use enumerate here instead of range(len)
    for experiment_idx, experiment_value in enumerate(
        tables.get("experiment_dna_short_read")
    ):
        if not experiment_value.get("experiment_sample_id"):
            for metadata_idx, metadata_value in enumerate(metadata):
                if metadata_value.get(
                    "experiment_dna_short_read_id"
                ) and experiment_value.get(
                    "experiment_dna_short_read_id"
                ) == metadata_value.get(
                    "experiment_dna_short_read_id"
                ):
                    tables.get("experiment_dna_short_read")[experiment_idx][
                        "experiment_sample_id"
                    ] = metadata[metadata_idx].get("sm_tag")

    for aligned_idx, aligned_value in enumerate(tables.get("aligned_dna_short_read")):
        if not aligned_value.get("aligned_dna_short_read_file"):
            for metadata_idx, metadata_value in enumerate(metadata):
                if metadata_value.get(
                    "aligned_dna_short_read_id"
                ) and aligned_value.get(
                    "aligned_dna_short_read_id"
                ) == metadata_value.get(
                    "aligned_dna_short_read_id"
                ):
                    if metadata_value.get("cram_file_name"):
                        cram_file_name = metadata_value.get("cram_file_name")
                        aligned_dna_short_read_file_path = f"{aligned_dna_short_read_files_path_header}/{cram_file_name}"
                        tables.get("aligned_dna_short_read")[aligned_idx][
                            "aligned_dna_short_read_file"
                        ] = aligned_dna_short_read_file_path
                    if metadata_value.get("crai_file_name"):
                        crai_file_name = metadata_value.get("crai_file_name")
                        aligned_dna_short_read_index_file_path = f"{aligned_dna_short_read_files_path_header}/{crai_file_name}"
                        tables.get("aligned_dna_short_read")[aligned_idx][
                            "aligned_dna_short_read_index_file"
                        ] = aligned_dna_short_read_index_file_path
                    if metadata_value.get("md5sum"):
                        tables.get("aligned_dna_short_read")[aligned_idx][
                            "md5sum"
                        ] = metadata[metadata_idx].get("md5sum")


def validate_tables(
    batch_number: str, gcp_bucket_name: str, issues: list[Issue], tables: list[Table]
):
    """Validates tables via normalization and checking uniqueness of values across tables"""
    ids = defaultdict(set)
    for table_name, samples in tables.items():
        # Validate sample by sample using cerberus
        samples = normalize_and_validate_samples(
            batch_number=batch_number,
            gcp_bucket=gcp_bucket_name,
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
    # Cross Reference Checks
    check_cross_references(ids, tables, issues)


def normalize_and_validate_samples(
    batch_number: str,
    gcp_bucket: str,
    issues: list[dict],
    samples: list[Sample],
    table_name: str,
):
    """Normalizes and validate samples"""
    schema = get_schema(table_name)
    sample_validator = SampleValidator(
        schema=schema, batch_number=batch_number, gcp_bucket=gcp_bucket
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
