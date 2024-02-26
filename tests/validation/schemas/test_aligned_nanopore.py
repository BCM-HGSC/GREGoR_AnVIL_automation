import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="aligned_nanopore_sample", scope="function")
def fixture_aligned_nanopore_sample():
    return {
        "aligned_nanopore_id": "BCM_ONTWGS_BHTEST_1_test-batch_id",
        "experiment_nanopore_id": "BCM_ONTWGS_BHTEST_1",
        "aligned_nanopore_file": "",
        "aligned_nanopore_index_file": "",
        "md5sum": "test-aligned_nanopore-gregor",
        "reference_assembly": "chm13",
        "alignment_software": "test-aligned_nanopore-gregor",
        "analysis_details": "test-aligned_nanopore-gregor",
        "mean_coverage": "NA",
        "genome_coverage": "NA",
        "contamination": "NA",
        "sex_concordance": "TRUE",
        "num_reads": "NA",
        "num_bases": "test-aligned_nanopore-gregor",
        "read_length_mean": "NA",
        "num_aligned_reads": "NA",
        "num_aligned_bases": "NA",
        "aligned_read_length_mean": "NA",
        "read_error_rate": "NA",
        "mapped_reads_pct": "NA",
        "methylation_called": "TRUE",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("aligned_nanopore")
    return SampleValidator(
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_aligned_nanopore_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a valid aligned_nanopore sample passes validation"""
    validator = get_validator
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_aligned_nanopore_id_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid aligned_nanopore_id fails validation"""
    validator = get_validator
    aligned_nanopore_sample["aligned_nanopore_id"] = "TEST-TEST"
    experiment_nanopore_id = aligned_nanopore_sample["experiment_nanopore_id"]
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {
        "aligned_nanopore_id": [
            f"Value must match the format of {experiment_nanopore_id}_test-batch_id"
        ]
    }


def test_experiment_nanopore_id_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid experiment_nanopore_id fails validation"""
    validator = get_validator
    aligned_nanopore_sample["experiment_nanopore_id"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {
        "aligned_nanopore_id": [
            "Value must match the format of TEST-TEST_test-batch_id"
        ],
        "experiment_nanopore_id": [
            "Value must end with _{some_number}",
            "Value must start with BCM_ONTWGS_BH",
        ],
    }


def test_mean_coverage_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid mean_coverage fails validation"""
    validator = get_validator
    aligned_nanopore_sample["mean_coverage"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"mean_coverage": ["Value must be NA or an int"]}


def test_mean_coverage_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a mean_coverage with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["mean_coverage"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_genome_coverage_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid genome_coverage fails validation"""
    validator = get_validator
    aligned_nanopore_sample["genome_coverage"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"genome_coverage": ["Value must be NA or an int"]}


def test_genome_coverage_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a genome_coverage with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["genome_coverage"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_contamination_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid contamination fails validation"""
    validator = get_validator
    aligned_nanopore_sample["contamination"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"contamination": ["Value must be NA or an int"]}


def test_contamination_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a contamination with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["contamination"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_num_reads_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid num_reads fails validation"""
    validator = get_validator
    aligned_nanopore_sample["num_reads"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"num_reads": ["Value must be NA or an int"]}


def test_num_reads_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a num_reads with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["num_reads"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_read_length_mean_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid read_length_mean fails validation"""
    validator = get_validator
    aligned_nanopore_sample["read_length_mean"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"read_length_mean": ["Value must be NA or an int"]}


def test_read_length_mean_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a read_length_mean with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["read_length_mean"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_num_aligned_reads_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid num_aligned_reads fails validation"""
    validator = get_validator
    aligned_nanopore_sample["num_aligned_reads"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"num_aligned_reads": ["Value must be NA or an int"]}


def test_num_aligned_reads_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a num_aligned_reads with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["num_aligned_reads"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_num_aligned_bases_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid num_aligned_bases fails validation"""
    validator = get_validator
    aligned_nanopore_sample["num_aligned_bases"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"num_aligned_bases": ["Value must be NA or an int"]}


def test_num_aligned_bases_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a num_aligned_bases with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["num_aligned_bases"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_aligned_read_length_mean_invalid_sample(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample with an invalid aligned_read_length_mean fails validation"""
    validator = get_validator
    aligned_nanopore_sample["aligned_read_length_mean"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {
        "aligned_read_length_mean": ["Value must be NA or an int"]
    }


def test_aligned_read_length_mean_is_int_valid_sample(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample with a aligned_read_length_mean with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["aligned_read_length_mean"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_read_error_rate_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid read_error_rate fails validation"""
    validator = get_validator
    aligned_nanopore_sample["read_error_rate"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"read_error_rate": ["Value must be NA or an int"]}


def test_read_error_rate_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a read_error_rate with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["read_error_rate"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_mapped_reads_pct_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid mapped_reads_pct fails validation"""
    validator = get_validator
    aligned_nanopore_sample["mapped_reads_pct"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"mapped_reads_pct": ["Value must be NA or an int"]}


def test_mapped_reads_pct_is_int_valid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with a mapped_reads_pct with a string number passes validation"""
    validator = get_validator
    aligned_nanopore_sample["mapped_reads_pct"] = "12345"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}


def test_aligned_nanopore_file_empty_normalization(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample's aligned_nanopore_file properly normalizes when empty to a path with coerce: aligned_nanopore_file"""
    validator = get_validator
    aligned_nanopore_id = aligned_nanopore_sample["aligned_nanopore_id"]
    aligned_nanopore_sample["aligned_nanopore_file"] = ""
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
    assert (
        validator.document["aligned_nanopore_file"]
        == f"gs://test-gcp-bucket/{aligned_nanopore_id}.bam"
    )


def test_aligned_nanopore_file_not_empty_normalization(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample's aligned_nanopore_file properly normalizes when not empty to the given value with coerce: aligned_nanopore_file"""
    validator = get_validator
    aligned_nanopore_sample["aligned_nanopore_file"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["aligned_nanopore_file"] == "TEST-TEST"


def test_aligned_nanopore_index_file_empty_normalization(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample's aligned_nanopore_index_file properly normalizes when empty to a path with coerce: aligned_nanopore_index_file"""
    validator = get_validator
    aligned_nanopore_id = aligned_nanopore_sample["aligned_nanopore_id"]
    aligned_nanopore_sample["aligned_nanopore_index_file"] = ""
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
    assert (
        validator.document["aligned_nanopore_index_file"]
        == f"gs://test-gcp-bucket/{aligned_nanopore_id}.bam.bai"
    )


def test_aligned_nanopore_index_file_not_empty_normalization(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample's aligned_nanopore_index_file properly normalizes when not empty to the given value with coerce: aligned_nanopore_index_file"""
    validator = get_validator
    aligned_nanopore_sample["aligned_nanopore_index_file"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["aligned_nanopore_index_file"] == "TEST-TEST"


def test_sex_concordance_normalization(get_validator, aligned_nanopore_sample):
    """Test that a sample's sex_concordance properly normalizes with coerce: uppercase"""
    validator = get_validator
    aligned_nanopore_sample["sex_concordance"] = "true"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["sex_concordance"] == "TRUE"


def test_methylation_called_normalization(get_validator, aligned_nanopore_sample):
    """Test that a sample's methylation_called properly normalizes with coerce: uppercase"""
    validator = get_validator
    aligned_nanopore_sample["methylation_called"] = "true"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["methylation_called"] == "TRUE"
