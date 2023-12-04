import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="aligned_dna_short_read_sample", scope="function")
def fixture_aligned_dna_short_read_sample():
    return {
        "aligned_dna_short_read_id": "BCM_BHTEST_test-batch_id",
        "experiment_dna_short_read_id": "BCM_BHTEST",
        "aligned_dna_short_read_file": "gs://test-gcp-bucket/BCM_BHTEST_test-batch_id.hgv.cram",
        "aligned_dna_short_read_index_file": "gs://test-gcp-bucket/BCM_BHTEST_test-batch_id.hgv.cram.crai",
        "md5sum": "test-aligned_dna_short_read-gregor",
        "reference_assembly": "GRCh38",
        "reference_assembly_uri": "NA",
        "reference_assembly_details": "test-aligned_dna_short_read-gregor",
        "alignment_software": "test-aligned_dna_short_read-gregor",
        "mean_coverage": "test-aligned_dna_short_read-gregor",
        "analysis_details": "test-aligned_dna_short_read-gregor",
        "quality_issues": "test-aligned_dna_short_read-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("aligned_dna_short_read")
    return SampleValidator(
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_aligned_dna_short_read_valid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a valid aligned_dna_short_read sample passes validation"""
    validator = get_validator
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}


def test_aligned_dna_short_read_id_invalid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample with an invalid aligned_dna_short_read_id fails validation"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_id"] = "TEST-TEST"
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {
        "aligned_dna_short_read_id": [
            "Value must start with BCM_ and end with _test-batch_id"
        ]
    }


def test_experiment_dna_short_read_id_invalid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample with an invalid experiment_dna_short_read_id fails validation"""
    validator = get_validator
    aligned_dna_short_read_sample["experiment_dna_short_read_id"] = "TEST-TEST"
    aligned_dna_short_read_id = aligned_dna_short_read_sample[
        "aligned_dna_short_read_id"
    ]
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {
        f"Value must match the format of {aligned_dna_short_read_id} minus _test-batch_id"
    }


def test_aligned_dna_short_read_file_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's aligned_dna_short_read_file properly normalizes with coerce: aligned_dna_short_read_file"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_file"] = "TEST-TEST"
    validator.normalized(aligned_dna_short_read_sample)
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}


def test_aligned_dna_short_read_index_file_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's aligned_dna_short_read_index_file properly normalizes with coerce: aligned_dna_short_read_index_file"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_index_file"] = "TEST-TEST"
    validator.normalized(aligned_dna_short_read_sample)
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}


def test_reference_assembly_uri_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's reference_assembly_uri properly normalizes with coerce: into_gcp_path_if_not_na"""
    validator = get_validator
    aligned_dna_short_read_sample["reference_assembly_uri"] = "TEST-TEST"
    validator.normalized(aligned_dna_short_read_sample)
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
