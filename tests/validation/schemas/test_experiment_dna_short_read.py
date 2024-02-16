import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="experiment_dna_short_read_sample", scope="function")
def fixture_experiment_dna_short_read_sample():
    return {
        "experiment_dna_short_read_id": "BCM_TEST",
        "analyte_id": "BCM_Subject_TEST_1_A1",
        "experiment_sample_id": "TEST",
        "seq_library_prep_kit_method": "test-experiment_dna_short_read-gregor",
        "read_length": "0",
        "experiment_type": "targeted",
        "targeted_regions_method": "test-experiment_dna_short_reade-gregor",
        "targeted_region_bed_file": "NA",
        "date_data_generation": "2023-12-25",
        "target_insert_size": "0",
        "sequencing_platform": "test-experiment_dna_short_read-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("experiment_dna_short_read")
    return SampleValidator(
        schema=schema, batch_number=1, gcp_bucket="test-gcp-bucket"
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
    assert validator.errors == {
        "experiment_dna_short_read_id": ["Value must start with BCM_"],
        "experiment_sample_id": ["Value must match the format of TEST-TEST minus BCM_"],
    }


def test_analyte_id_invalid_sample(get_validator, experiment_dna_short_read_sample):
    """Test that a sample with an invalid anlyte_id fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["analyte_id"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with BCM_Subject_ and ends with _1_A, _2_A, _3_A, or _4_A and then a number between 1 and 1, inclusively",
        ]
    }


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
        "experiment_sample_id": [
            f"Value must match the format of {experiment_dna_short_read_id} minus BCM_"
        ]
    }


def test_read_length_invalid_sample(get_validator, experiment_dna_short_read_sample):
    """Test that a sample with an invalid read_length fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["read_length"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {"read_length": ["Value requires an int"]}


def test_target_insert_size_invalid_sample(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample with an invalid target_insert_size fails validation"""
    validator = get_validator
    experiment_dna_short_read_sample["target_insert_size"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {"target_insert_size": ["Value requires an int"]}


def test_experiment_type_normalization(get_validator, experiment_dna_short_read_sample):
    """Test that a sample's experiment_type properly normalizes with coerce: lowercase"""
    validator = get_validator
    experiment_dna_short_read_sample["experiment_type"] = "TARGETED"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}
    assert validator.document["experiment_type"] == "targeted"


def test_targeted_region_bed_file_normalization(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample's targeted_region_bed_file properly normalizes with coerce: into_gcp_path_if_not_na"""
    validator = get_validator
    experiment_dna_short_read_sample["targeted_region_bed_file"] = "TEST-TEST"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}
    assert (
        validator.document["targeted_region_bed_file"]
        == "gs://test-gcp-bucket/TEST-TEST"
    )


def test_date_data_generation_normalization(
    get_validator, experiment_dna_short_read_sample
):
    """Test that a sample's date_data_generation properly normalizes with coerce: year_month_date"""
    validator = get_validator
    experiment_dna_short_read_sample["date_data_generation"] = "12-25-2023"
    validator.validate(experiment_dna_short_read_sample)
    assert validator.errors == {}
    assert validator.document["date_data_generation"] == "2023-12-25"
