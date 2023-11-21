from pathlib import Path
from typing import Set

from addict import Dict

from gregor_anvil_automation.utils.utils import get_table_samples
from ..utils.types import Sample
from ..utils.issue import Issue
from ..validation.schema import get_schema
from ..validation.sample import SampleValidator
from ..validation.checks import *


def run(config: Dict, excel_path: Path) -> int:
    """The short_reads entry point"""
    tables = get_table_samples(excel_path)
    # import pprint

    # pprint.pprint(tables["participant"])
    issues = []
    # Validate files
    for table_name, samples in tables.items():
        issues = validate_table(table_name, samples)

    # If all ok, generate tsvs

    # If any errors, email issues

    # If all is good, email of success and files generated

    return 0


def validate_table(table_name: str, samples: list[Sample]) -> list[Issue]:
    """Validates a table and returns a list of issues, if any found."""
    issues = []
    # Validate table wide issues
    get_table_wide_issues()
    # Validate sample by sample using cerberus
    # Load schema
    schema = get_schema(table_name)
    sample_validator = SampleValidator(schema)
    for sample in samples:
        sample_validator.validate(sample)
        issues.extend(
            convert_errors_to_issues(
                errors=sample_validator.errors, table_name=table_name, row=sample["row"]
            )
        )
    return issues


def get_table_wide_issues():
    """Returns issues if"""
    # Check uniqueness..
    # Check all the things


def convert_errors_to_issues(errors: list[dict], **kwargs) -> list[dict[str, str]]:
    """Convers from Cerberus errors to a dictionary of issues. We use the
    biobank_id, lims_id, and sample_id since a manifest is guaranteed to have
    at least one of these fields."""
    issues = []
    for field, messages in errors.items():
        for message in messages:
            # logger.error("%s: %s", field, message)
            issue = Issue(
                **kwargs,
                field=field,
                message=message,
            )
            issues.append(issue)
    return issues
