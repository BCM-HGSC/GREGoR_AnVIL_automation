"""Custom checks that we can't do with cerberus"""

from collections import defaultdict
from logging import getLogger

from gregor_anvil_automation.utils.issue import Issue
from ..utils.types import Sample, Table
from ..utils.mappings import CROSS_REF_CHECK, UNIQUE_MAPPING

logger = getLogger(__name__)


def check_uniqueness(samples: list[Sample], table_name: str, issues: list[Issue]):
    """Checks if the given list of values is unique"""
    fields_to_check = UNIQUE_MAPPING.get(table_name)
    if fields_to_check and samples:
        for field in fields_to_check:
            logger.info(
                "Verifying Uniqueness of Field %s in Table %s", field, table_name
            )
            unique_values = set()
            for sample in samples:
                if field in sample:
                    value = sample.get(field)
                    if value in unique_values:
                        new_issue = Issue(
                            field,
                            f"The value of {field} has a duplicate in the table {table_name}",
                            table_name,
                            sample["row_number"],
                        )
                        logger.error(new_issue)
                        issues.append(new_issue)
                    else:
                        unique_values.add(value)


def check_value_exist_in_source(field_name: str, table: Table, table_source: Table):
    """Checks that the values given exist in the source table.
    Example if participant table has family_id BCM_Fam_1234, this checks
    that BCM_Fam_1234 exist in the family table under `family_id`"""
    error = f"Value does not exist in the table {field_name}"
    field_values = {sample[field_name] for sample in table_source}
    invalid = set()
    for sample in table:
        value = sample[field_name]
        if value not in field_values:
            invalid.add(value)
            return False, error
    return True


def check_cross_references(ids: defaultdict, tables: list[Table], issues: list[Issue]):
    """Checks all the foreign keys exist in the primary table"""
    for table_name, source_field, dest_field in CROSS_REF_CHECK:
        if table_name not in tables:
            continue

        missing_values = set()
        for sample in tables[table_name]:
            values = sample[dest_field].split("|")
            for value in values:
                if value.lower() != "na" and value not in ids[source_field]:
                    missing_values.add(value)

        if missing_values:
            issues.append(
                Issue(
                    field=dest_field,
                    message=f"Foreign keys does not exist in original table {missing_values}",
                    table_name=table_name,
                    row=None,
                )
            )
