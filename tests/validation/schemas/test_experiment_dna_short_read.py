import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="experiment_dna_short_read_sample", scope="function")
def fixture_experiment_dna_short_read_sample():
    return {
        "experiment_dna_short_read_id": "BCM_TEST",
        "analyte_id": "test-analyte-gregor",
        "experiment_sample_id": "TEST",
        "seq_library_prep_kit_method": "test-analyte-gregor",
        "read_length": "0",
        "experiment_type": "targeted",
        "targeted_regions_method": "test-analyte-gregor",
        "targeted_region_bed_file": "NA",
        "date_data_generation": "2023-12-01",
        "target_insert_size": "0",
        "sequencing_platform": "test-analyte-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("experiment_dna_short_read")
    return SampleValidator(
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_experiment_dna_short_read_valid_sample(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a valid experiment_dna_short_read sample passes validation"""
    validator = get_validator
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}


def test_experiment_dna_short_read_id_invalid_sample(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample with an invalid experiment_dna_short_read_id fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["experiment_dna_short_read_id"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {"Value must start with BCM_"}


def test_experiment_sample_id_invalid_sample(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample with an invalid experiment_sample_id fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["experiment_sample_id"] = "TEST-TEST"
    experiment_dna_short_read_id = experiment_dna_short_read_sample[
        "experiment_dna_short_read_id"
    ]
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {
        f"Value must match the format of {experiment_dna_short_read_id} minus BCM_"
    }


def test_read_length_invalid_sample(get_validator, experiment_dna_short_read_sample):
    """Test that a sample with an invalid read_length fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["read_length"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {"Value requires an int"}


def test_target_insert_size_invalid_sample(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample with an invalid target_insert_size fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["target_insert_size"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {"Value requires an int"}


def test_experiment_type_normalization(get_validator, experiment_dna_short_read_sample):
    """Test that a sample's experiment_type properly normalizes"""
    validator = get_validator
    experiment_dna_short_read_sample["experiment_type"] = "TARGETED"
    validator.normalized(experiment_dna_short_read_sample)
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}


def test_targeted_region_bed_file_normalization(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample's targeted_region_bed_file properly normalizes"""
    validator = get_validator
    experiment_dna_short_read_sample["targeted_region_bed_file"] = "TEST-TEST"
    validator.normalized(experiment_dna_short_read_sample)
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}


def test_date_data_generation_normalization(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample's date_data_generation properly normalizes"""
    validator = get_validator
    experiment_dna_short_read_sample["date_data_generation"] = "12-01-2023"
    validator.normalized(experiment_dna_short_read_sample)
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}
