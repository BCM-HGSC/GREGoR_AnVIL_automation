import addict
import pytest

from gregor_anvil_automation.validation.checks import check_uniqueness


@pytest.fixture(name="uniqueness_sample", scope="function")
def fixture_uniqueness_sample():
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
        }
    )


@pytest.fixture(name="uniqueness_sample2", scope="function")
def fixture_uniqueness_sample2():
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
        }
    )


@pytest.fixture(name="aligned_dna_short_read", scope="function")
def fixture_uniqueness_table_no_issues(uniqueness_sample, uniqueness_sample2):
    return [
        uniqueness_sample,
        uniqueness_sample2,
    ]


@pytest.fixture(name="AlignedShortRead", scope="function")
def fixture_uniqueness_table_issues(uniqueness_sample):
    return [
        uniqueness_sample,
        uniqueness_sample,
    ]


def test_check_uniqueness_no_issues(aligned_dna_short_read):
    """Test that check_uniqueness sample passes validation with no issues"""
    table_name = "aligned_dna_short_read"
    table = aligned_dna_short_read
    issues = []
    issues = check_uniqueness(table, table_name, issues)
    assert issues == []


def test_check_uniqueness_sample_issues_no_initial_issues(uniqueness_sample):
    """Test that check_uniqueness sample passes validation with sample issues"""
    table_name = "aligned_dna_short_read"
    samples = [uniqueness_sample, uniqueness_sample]
    value = "aligned_dna_short_read_id"
    row = 1
    issues = []
    issues = check_uniqueness(samples, table_name, issues)
    assert issues == set(
        {
            "aligned_dna_short_read_id",
            f"Value {value} already exists in the table {table_name} in row {row}",
            "uniqueness_table_issues",
            row,
        }
    )


def test_check_uniqueness_initial_issues_no_sample_issues(AlignedShortRead):
    """Test that check_uniqueness sample passes validation with initial issues"""
    table_name = "AlignedShortRead"
    table = AlignedShortRead
    value = "aligned_dna_short_read_id"
    row = 1
    issues = set(
        [
            "aligned_dna_short_read_id",
            f"test-issue with {value}",
            table_name,
            row,
        ]
    )
    issues = check_uniqueness(table, table_name, issues)
    assert issues == set(
        {
            "aligned_dna_short_read_id",
            f"test-issue with {value}",
            table_name,
            row,
        }
    )


def test_check_uniqueness_initial_issues_and_sample_issues(AlignedShortRead):
    """Test that check_uniqueness sample passes validation with initial issues and sample issues"""
    table_name = "AlignedShortRead"
    table = AlignedShortRead
    value = "aligned_dna_short_read_id"
    row = 1
    issues = set(
        [
            "aligned_dna_short_read_id",
            f"test-issue with {value}",
            table_name,
            row,
        ]
    )
    issues = check_uniqueness(table, table_name, issues)
    assert issues == [
        set(
            {
                "aligned_dna_short_read_id",
                f"test-issue with {value}",
                table_name,
                row,
            }
        ),
        set(
            {
                "aligned_dna_short_read_id",
                f"Value {value} already exists in the table {table_name} in row {row}",
                table_name,
                row,
            }
        ),
    ]
