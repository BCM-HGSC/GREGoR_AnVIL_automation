"""Custom checks that we can't do with cerberus"""
from gregor_anvil_automation.utils.issue import Issue
from ..utils.types import Sample, Table
from ..utils.mappings import UNIQUE_MAPPING


def check_uniqueness(samples: list[Sample], table_name: str, issues: list[Issue]):
    """Checks if the given list of values is unique"""
    # TODO: Work on this given the new input. It will not return anything but
    # add on to the existing ongoing issues list. I recommend using test
    # as you develop this so you can get instant feedback.
    # Use the UNIQUE_MAPPING dict given
    table = samples.get(table_name)
    if table and table in UNIQUE_MAPPING:
        for value in table:
            if table.count(value) > 1:
                row = table.index(value)
                new_issue = Issue[
                    table,
                    f"Value {value} already exists in the table {table_name} in row {row}",
                    table_name,
                    row,
                ]
                issues.append(new_issue)
                return False
    return True


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
