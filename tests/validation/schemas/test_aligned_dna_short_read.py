import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="aligned_dna_short_read_sample", scope="function")
def fixture_aligned_dna_short_read_sample():
    return {
        "aligned_dna_short_read_id": "BCM_BHTEST_test-batch_number",
        "experiment_dna_short_read_id": "BCM_BHTEST",
        "aligned_dna_short_read_file": "",
        "aligned_dna_short_read_index_file": "",
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
        schema=schema, batch_number="test-batch_number", gcp_bucket="test-gcp-bucket"
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
            "Value must start with BCM_ and end with _test-batch_number"
        ],
        "experiment_dna_short_read_id": [
            "Value must match the format of TEST-TEST minus _test-batch_number"
        ],
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
        "experiment_dna_short_read_id": [
            f"Value must match the format of {aligned_dna_short_read_id} minus _test-batch_number"
        ]
    }


def test_aligned_dna_short_read_file_empty_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's aligned_dna_short_read_file properly normalizes when empty to a path with coerce: aligned_dna_short_read_file"""
    validator = get_validator
    aligned_dna_short_read_id = aligned_dna_short_read_sample[
        "aligned_dna_short_read_id"
    ]
    aligned_dna_short_read_sample["aligned_dna_short_read_file"] = ""
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
    assert (
        validator.document["aligned_dna_short_read_file"]
        == f"gs://test-gcp-bucket/{aligned_dna_short_read_id}.hgv.cram"
    )


def test_aligned_dna_short_read_file_not_empty_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's aligned_dna_short_read_file properly normalizes when not empty to the given value with coerce: aligned_dna_short_read_file"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_file"] = "TEST-TEST"
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
    assert validator.document["aligned_dna_short_read_file"] == "TEST-TEST"


def test_aligned_dna_short_read_index_file_empty_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's aligned_dna_short_read_index_file properly normalizes when empty to path with coerce: aligned_dna_short_read_index_file"""
    validator = get_validator
    aligned_dna_short_read_id = aligned_dna_short_read_sample[
        "aligned_dna_short_read_id"
    ]
    aligned_dna_short_read_sample["aligned_dna_short_read_index_file"] = ""
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
    assert (
        validator.document["aligned_dna_short_read_index_file"]
        == f"gs://test-gcp-bucket/{aligned_dna_short_read_id}.hgv.cram.crai"
    )


def test_aligned_dna_short_read_index_file_not_empty_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's aligned_dna_short_read_index_file properly normalizes when not empty to the given value with coerce: aligned_dna_short_read_index_file"""
    validator = get_validator
    aligned_dna_short_read_sample["aligned_dna_short_read_index_file"] = "TEST-TEST"
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
    assert validator.document["aligned_dna_short_read_index_file"] == "TEST-TEST"


def test_reference_assembly_uri_na_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's reference_assembly_uri properly normalizes to 'NA' with coerce: into_gcp_path_if_not_na"""
    validator = get_validator
    aligned_dna_short_read_sample["reference_assembly_uri"] = "NA"
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
    assert validator.document["reference_assembly_uri"] == "NA"


def test_reference_assembly_uri_gcp_path_normalization(
    get_validator, aligned_dna_short_read_sample
):
    """Test that a sample's reference_assembly_uri properly normalizes to a path with coerce: into_gcp_path_if_not_na"""
    validator = get_validator
    aligned_dna_short_read_sample["reference_assembly_uri"] = "TEST-TEST"
    validator.validate(aligned_dna_short_read_sample)
    assert validator.errors == {}
    assert (
        validator.document["reference_assembly_uri"] == "gs://test-gcp-bucket/TEST-TEST"
    )
