from collections import defaultdict

import pytest

from gregor_anvil_automation.utils.issue import Issue
from gregor_anvil_automation.validation.checks import check_cross_references


# Minimal tables with valid samples
@pytest.fixture(name="valid_tables")
def fixture_valid_tables():
    return {
        "participant": [
            {
                "participant_id": "test-participant_id-001",
                "family_id": "test-family_id-001",
            }
        ],
        "analyte": [
            {
                "participant_id": "test-participant_id-001",
                "analyte_id": "test-analyte_id-001",
            }
        ],
        "family": [{"family_id": "test-family_id-001"}],
    }


def test_check_cross_table_ref_no_issues(
    valid_tables: dict,
):
    """Test that no issues returned if the source table contains the foreign
    keys in the given table."""
    issues = []
    ids = defaultdict(set)
    ids["participant_id"] = {"test-participant_id-001"}
    ids["family_id"] = {"test-family_id-001"}
    check_cross_references(ids, valid_tables, issues)
    assert not issues


def test_check_cross_table_ref_referenced_table_not_given(
    valid_tables: dict,
):
    """Test that an error is returned even if the referenced table is not given.
    This is a designed choice.

    Ex: If participant has `family_id` we do expect a table with `family.family_id`
    """
    issues = []
    ids = defaultdict(set)
    ids["participant_id"] = {"test-participant_id-001"}
    valid_tables.pop("family")
    check_cross_references(ids, valid_tables, issues)
    assert issues == [
        Issue(
            field="family_id",
            message="Foreign keys does not exist in original table {'test-family_id-001'}",
            table_name="participant",
            row=None,
        )
    ]


def test_check_cross_table_ref_verify_table_skip():
    """if the table is not a table in the `CROSS_REF_CHECK` (one that does not
    need to be checked), that no issues are returned
    """
    issues = []
    ids = defaultdict(set)
    ids["participant_id"] = {"test-participant_id-001"}
    valid_tables = {"some-made-up-table": "test-madeup-id-001"}
    check_cross_references(ids, valid_tables, issues)
    assert not issues
