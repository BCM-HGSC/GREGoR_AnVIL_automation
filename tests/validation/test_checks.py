from collections import defaultdict

import addict
import pytest

from gregor_anvil_automation.utils.issue import Issue
from gregor_anvil_automation.validation.checks import check_cross_references, check_uniqueness


@pytest.fixture(name="uniqueness_sample_valid_2", scope="function")
def fixture_uniqueness_sample_valid_2():
    return addict.Dict(
        {
            "aligned_dna_short_read_id": "BCM_BHTEST_test-batch_id",
            "experiment_dna_short_read_id": "BCM_BHTEST",
            "aligned_dna_short_read_file": "",
            "aligned_dna_short_read_index_file": "",
            "md5sum": "test-uniqueness-gregor",
            "reference_assembly": "GRCh38",
            "reference_assembly_uri": "NA",
            "reference_assembly_details": "test-uniqueness-gregor",
            "alignment_software": "test-uniqueness-gregor",
            "mean_coverage": "test-uniqueness-gregor",
            "analysis_details": "test-uniqueness-gregor",
            "quality_issues": "test-uniqueness-gregor",
            "row_number": 2,
        }
    )


@pytest.fixture(name="uniqueness_sample_invalid_3", scope="function")
def fixture_uniqueness_sample_invalid_3():
    return addict.Dict(
        {
            "aligned_dna_short_read_id": "BCM_BHTEST_test-batch_id",
            "experiment_dna_short_read_id": "BCM_BHTEST",
            "aligned_dna_short_read_file": "",
            "aligned_dna_short_read_index_file": "",
            "md5sum": "test-uniqueness-gregor",
            "reference_assembly": "GRCh38",
            "reference_assembly_uri": "NA",
            "reference_assembly_details": "test-uniqueness-gregor",
            "alignment_software": "test-uniqueness-gregor",
            "mean_coverage": "test-uniqueness-gregor",
            "analysis_details": "test-uniqueness-gregor",
            "quality_issues": "test-uniqueness-gregor",
            "row_number": 3,
        }
    )


@pytest.fixture(name="uniqueness_sample_valid_3", scope="function")
def fixture_uniqueness_sample_valid_3():
    return addict.Dict(
        {
            "aligned_dna_short_read_id": "BCM_BHTEST2_test-batch_id",
            "experiment_dna_short_read_id": "BCM_BHTEST2",
            "aligned_dna_short_read_file": "",
            "aligned_dna_short_read_index_file": "",
            "md5sum": "test-uniqueness-gregor2",
            "reference_assembly": "GRCh38",
            "reference_assembly_uri": "NA",
            "reference_assembly_details": "test-uniqueness-gregor2",
            "alignment_software": "test-uniqueness-gregor2",
            "mean_coverage": "test-uniqueness-gregor2",
            "analysis_details": "test-uniqueness-gregor2",
            "quality_issues": "test-uniqueness-gregor2",
            "row_number": 3,
        }
    )


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


def test_check_uniqueness_no_issues(
    uniqueness_sample_valid_2, uniqueness_sample_valid_3
):
    """Test that check_uniqueness sample passes validation with no issues"""
    table_name = "aligned_dna_short_read"
    samples = [uniqueness_sample_valid_2, uniqueness_sample_valid_3]
    issues = []
    check_uniqueness(samples, table_name, issues)
    assert issues == []


def test_check_uniqueness_sample_issues_no_initial_issues(
    uniqueness_sample_valid_2, uniqueness_sample_invalid_3
):
    """Test that check_uniqueness sample passes validation with sample issues"""
    table_name = "aligned_dna_short_read"
    samples = [uniqueness_sample_valid_2, uniqueness_sample_invalid_3]
    value = "aligned_dna_short_read_id"
    row = uniqueness_sample_invalid_3["row_number"]
    issues = []
    check_uniqueness(samples, table_name, issues)
    print(issues)
    assert issues == [
        Issue(
            f"{value}",
            f"Value {value} already exists in the table {table_name} in row {row}",
            table_name,
            row,
        ),
        Issue(
            "experiment_dna_short_read_id",
            f"Value experiment_dna_short_read_id already exists in the table {table_name} in row {row}",
            table_name,
            row,
        ),
    ]


def test_check_uniqueness_initial_issues_no_sample_issues(
    uniqueness_sample_valid_2, uniqueness_sample_valid_3
):
    """Test that check_uniqueness sample passes validation with initial issues"""
    table_name = "aligned_dna_short_read"
    samples = [uniqueness_sample_valid_2, uniqueness_sample_valid_3]
    value = "aligned_dna_short_read_id"
    row = uniqueness_sample_valid_3["row_number"]
    issues = [
        Issue(
            "aligned_dna_short_read_id",
            f"test-issue with {value}",
            table_name,
            row,
        )
    ]
    check_uniqueness(samples, table_name, issues)
    assert issues == [
        Issue(
            "aligned_dna_short_read_id",
            f"test-issue with {value}",
            table_name,
            row,
        )
    ]


def test_check_uniqueness_initial_issues_and_sample_issues(
    uniqueness_sample_valid_2, uniqueness_sample_invalid_3
):
    """Test that check_uniqueness sample passes validation with initial issues and sample issues"""
    table_name = "aligned_dna_short_read"
    samples = [uniqueness_sample_valid_2, uniqueness_sample_invalid_3]
    value = "aligned_dna_short_read_id"
    row = uniqueness_sample_invalid_3["row_number"]
    issues = [
        Issue(
            f"{value}",
            f"test-issue with {value}",
            table_name,
            row,
        )
    ]
    check_uniqueness(samples, table_name, issues)
    assert issues == [
        Issue(
            f"{value}",
            f"test-issue with {value}",
            table_name,
            row,
        ),
        Issue(
            f"{value}",
            f"Value {value} already exists in the table {table_name} in row {row}",
            table_name,
            row,
        ),
        Issue(
            "experiment_dna_short_read_id",
            f"Value experiment_dna_short_read_id already exists in the table {table_name} in row {row}",
            table_name,
            row,
        ),
    ]


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