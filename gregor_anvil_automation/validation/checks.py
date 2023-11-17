"""Custom checks that we can't do with cerberus"""
from ..utils.types import Table


def check_uniqueness(samples: list[str]):
    """Checks if the given list of values is unique"""
    error = []
    # TODO: Add code
    for sample in samples:
        other_id = sample[f"{id_name}"]
        if other_id in subject_ids:
            error_message = f"ID is already present in {samples}"
            print(error_message)
            errors.append(error_message)
    return False


def check_value_exist_in_source(field_name: str, table: Table, table_source: Table):
    """Checks that the values given exist in the source table.
    Example if participant table has family_id BCM_Fam_1234, this checks
    that BCM_Fam_1234 exist in the family table under `family_id`"""
    field_values = {sample[field_name] for sample in table_source}
    invalid = {}
    for sample in table:
        value = sample[field_name]
        if value not in field_values:
            invalid.add(value)
            return False, error
    return True
