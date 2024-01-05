import addict
import pytest

from gregor_anvil_automation.utils.issue import Issue
from gregor_anvil_automation.validation.checks import check_uniqueness


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
