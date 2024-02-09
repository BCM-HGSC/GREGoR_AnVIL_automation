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


def run(config: Dict, excel_path: Path, batch_id: str, working_dir: Path) -> int:
    """The short_reads entry point"""
    tables = get_table_samples(excel_path)
    issues = []
    # Validate files
    validate_tables(
        batch_id=batch_id,
        gcp_bucket_name=config.gcp_bucket_name,
        issues=issues,
        tables=tables,
    )

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


def validate_tables(
    batch_id: str, gcp_bucket_name: str, issues: list[Issue], tables: list[Table]
):
    """Validates tables via normalization and checking uniqueness of values across tables"""
    ids = defaultdict(set)
    for table_name, samples in tables.items():
        # Validate sample by sample using cerberus
        samples = normalize_and_validate_samples(
            batch_id=batch_id,
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
    batch_id: str,
    gcp_bucket: str,
    issues: list[dict],
    samples: list[Sample],
    table_name: str,
):
    """Normalizes and validate samples"""
    schema = get_schema(table_name)
    sample_validator = SampleValidator(
        schema=schema, batch_id=batch_id, gcp_bucket=gcp_bucket
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
