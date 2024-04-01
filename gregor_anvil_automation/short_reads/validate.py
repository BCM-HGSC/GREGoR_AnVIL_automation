from collections import defaultdict
from pathlib import Path
from dataclasses import asdict
from logging import getLogger

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
from ..utils.mappings import HEADER_CASE_SENSITIVE_MAP


logger = getLogger(__name__)


def run(config: Dict, input_path: Path, batch_number: str, working_dir: Path) -> int:
    """The short_reads entry point"""
    logger.info("Retrieving Table Samples")
    tables = get_table_samples(input_path)
    issues = []
    # Validate files
    logger.info("Validating Tables")
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
        logger.info("Generating Issue Files")
        generate_file(file_path, data_headers, [asdict(issue) for issue in issues], ",")
        logger.info("Sending Issues Email")
        send_email(config["email"], subject, ATTACHED_ISSUES_MSG_BODY, [file_path])
        return 1
    file_paths = []
    logger.info("Generating Table Files")
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
    logger.info("Sending Table Files Email")
    send_email(config["email"], subject, SUCCESS_MSG_BODY, file_paths)
    return 0


def validate_tables(batch_number: str, issues: list[Issue], tables: list[Table]):
    """Validates tables via normalization and checking uniqueness of values across tables"""
    ids = defaultdict(set)
    for table_name, samples in tables.items():
        # Validate sample by sample using cerberus
        logger.info("Normalizing and Validating Samples")
        samples = normalize_and_validate_samples(
            batch_number=batch_number,
            issues=issues,
            samples=samples,
            table_name=table_name,
        )
        # Validate Table Wide Issues which as of now is just unique checking
        logger.info("Verifying Sample Field Uniqueness")
        check_uniqueness(samples, table_name, issues)
        if table_name in REFERENCE_SOURCE:
            ids[REFERENCE_SOURCE[table_name]].update(
                sample[REFERENCE_SOURCE[table_name]] for sample in samples
            )
        tables[table_name] = samples
    # Cross Reference Checks
    logger.info("Verifying Primary Table Foreign Key Existence")
    check_cross_references(ids, tables, issues)


def normalize_and_validate_samples(
    batch_number: str,
    issues: list[dict],
    samples: list[Sample],
    table_name: str,
):
    """Normalizes and validate samples"""
    logger.info("Retreiving Schema")
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
