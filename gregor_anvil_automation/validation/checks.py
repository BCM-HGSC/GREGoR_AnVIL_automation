"""Custom checks that we can't do with cerberus"""
from gregor_anvil_automation.utils.issue import Issue
from ..utils.types import Sample, Table
from ..utils.mappings import UNIQUE_MAPPING, TABLE_NAME_MAPPINGS


def check_uniqueness(samples: list[Sample], table_name: str, issues: list[Issue]):
    """Checks if the given list of values is unique"""
    if TABLE_NAME_MAPPINGS.get(table_name):
        table_name = TABLE_NAME_MAPPINGS.get(table_name)
    if UNIQUE_MAPPING.get(table_name) and samples:
        for key in UNIQUE_MAPPING.get(table_name):
            unique_values = []
            if key in samples:
                print(key)
                print(samples)
                for sample in samples:
                    value = sample.get(key)
                    if value in unique_values:
                        row = list(sample.keys()).index(key)
                        new_issue = Issue[
                            key,
                            f"Value {key} already exists in the table {table_name} in row {row}",
                            table_name,
                            row,
                        ]
                        issues.append(new_issue)
                    else:
                        unique_values.append(value)
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
