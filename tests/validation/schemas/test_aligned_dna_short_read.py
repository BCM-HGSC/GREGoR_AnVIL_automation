import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="aligned_dna_short_read_sample", scope="function")
def fixture_aligned_dna_short_read_sample():
    return {
        "aligned_dna_short_read_id": "BCM_BHTEST",
        "experiment_dna_short_read_id": "BCM_BHTEST",
        "aligned_dna_short_read_file": "gs://test-gcp-bucket/BCM_BHTEST.hgv.cram",
        "aligned_dna_short_read_index_file": "gs://test-gcp-bucket/BCM_BHTEST.hgv.cram.crai",
        "md5sum": "test-aligned_dna_short_read_id-gregor",
        "reference_assembly": "GRCh38",
        "reference_assembly_uri": "NA",
        "reference_assembly_details": "test-aligned_dna_short_read_id-gregor",
        "alignment_software": "test-aligned_dna_short_read_id-gregor",
        "mean_coverage": "test-aligned_dna_short_read_id-gregor",
        "analysis_details": "test-aligned_dna_short_read_id-gregor",
        "quality_issues": "test-aligned_dna_short_read_id-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("aligned_dna_short_read")
    return SampleValidator(
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_aligned_dna_short_read_id_valid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that an aligned_dna_short_read_id sample passes validation"""
    validator = get_validator
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}


def test_aligned_dna_short_read_id_invalid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that an invalid aligned_dna_short_read_id sample fails validation"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_id"] = "TEST-TEST"
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {
        "aligned_dna_short_read_id": ["Value must start with BCM_"]
    }


def test_experiment_dna_short_read_id_valid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that an experiment_dna_short_read_id sample passes validation"""
    validator = get_validator
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}


def test_experiment_dna_short_read_id_invalid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that an invalid experiment_dna_short_read_id sample fails validation"""
    validator = get_validator
    aligned_dna_short_read_sample["experiment_dna_short_read_id"] = "TEST-TEST"
    aligned_dna_short_read_id = aligned_dna_short_read_sample[
        "aligned_dna_short_read_id"
    ]
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {
        "experiment_dna_short_read_id": [
            f"Value must match the format of {aligned_dna_short_read_id} minus _test-batch_id"
        ]
    }


def test_aligned_dna_short_read_file_valid_sample(
    get_validator, aligned_dna_short_read_sample
):
    """Test that an aligned_dna_short_read_file sample normalizes properly"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_file"] = "TEST-TEST"
    validator.normalized(aligned_dna_short_read_sample)
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
