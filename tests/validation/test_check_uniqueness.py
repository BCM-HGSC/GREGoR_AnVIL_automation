import pytest

from gregor_anvil_automation.validation.checks import check_uniqueness


@pytest.fixture(name="uniqueness_table", scope="function")
def fixture_uniqueness_table():
    return [
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
        },
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
        },
    ]


@pytest.fixture(name="uniqueness_sample", scope="function")
def fixture_uniqueness_sample():
    return {
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


def test_check_uniqueness_no_issues(uniqueness_sample, uniqueness_table):
    """Test that check_uniqueness sample passes validation with no issues"""
    table = uniqueness_table
    sample = uniqueness_sample
    issues = []
    check_uniqueness(sample, table, issues)
    assert issues == []


def test_check_uniqueness_sample_issues_no_initial_issues(
    uniqueness_sample, uniqueness_table
):
    """Test that check_uniqueness sample passes validation with sample issues"""
    table = [
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
        },
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
        },
    ]
    sample = uniqueness_sample
    issues = []
    row = uniqueness_table[1]["aligned_dna_short_read_id"]
    check_uniqueness(sample, table, issues)
    assert issues == {
        table,
        f"Value aligned_dna_short_read_id already exists in the table uniqueness_table in row {row}",
        "uniqueness_table",
        row,
    }


def test_check_uniqueness_initial_issues_no_sample_issues(
    uniqueness_sample, uniqueness_table
):
    """Test that check_uniqueness sample passes validation with initial issues"""
    table = uniqueness_table
    sample = uniqueness_sample
    row = uniqueness_table[1]["aligned_dna_short_read_id"]
    issues = [
        table,
        f"test-issue with aligned_dna_short_read_id",
        "uniqueness_table",
        row,
    ]
    check_uniqueness(sample, table, issues)
    assert issues == {
        table,
        f"test-issue with aligned_dna_short_read_id",
        "uniqueness_table",
        row,
    }


def test_check_uniqueness_initial_issues_and_sample_issues(
    uniqueness_sample, uniqueness_table
):
    """Test that check_uniqueness sample passes validation with initial issues and sample issues"""
    table = [
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
        },
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
        },
    ]
    sample = uniqueness_sample
    row = uniqueness_table[1]["aligned_dna_short_read_id"]
    issues = [
        table,
        f"test-issue with aligned_dna_short_read_id",
        "uniqueness_table",
        row,
    ]
    check_uniqueness(sample, table, issues)
    assert issues == {
        {table, f"test-issue with aligned_dna_short_read_id", "uniqueness_table", row},
        {
            table,
            f"Value aligned_dna_short_read_id already exists in the table uniqueness_table in row {row}",
            "uniqueness_table",
            row,
        },
    }
