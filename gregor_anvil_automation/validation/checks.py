"""Custom checks that we can't do with cerberus"""
from gregor_anvil_automation.utils.issue import Issue
from ..utils.types import Sample, Table
from ..utils.mappings import UNIQUE_MAPPING


def check_uniqueness(samples: list[Sample], table_name: str, issues: list[Issue]):
    """Checks if the given list of values is unique"""
    fields_to_check = UNIQUE_MAPPING.get(table_name)
    if fields_to_check and samples:
        for field in fields_to_check:
            unique_values = set()
            for sample in samples:
                if field in sample:
                    value = sample.get(field)
                    if value in unique_values:
                        new_issue = Issue[
                            field,
                            f"Value {field} already exists in the table {table_name} in row {sample.row_number}",
                            table_name,
                            sample.row_number,
                        ]
                        issues.append(new_issue)
                    else:
                        unique_values.add(value)
    return issues


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
