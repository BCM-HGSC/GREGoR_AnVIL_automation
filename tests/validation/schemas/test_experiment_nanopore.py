import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="experiment_nanopore_sample", scope="function")
def fixture_experiment_nanopore_sample():
    return {
        "experiment_nanopore_id": "BCM_ONTWGS_TEST",
        "analyte_id": "BCM_Subject_TEST_1_test-batch_id",
        "experiment_sample_id": "test-experiment_nanopore-gregor",
        "seq_library_prep_kit_method": "LSK109",
        "fragmentation_method": "test-experiment_nanopore-gregor",
        "experiment_type": "targeted",
        "targeted_regions_method": "test-experiment_nanopore-gregor",
        "targeted_region_bed_file": "test-experiment_nanopore-gregor",
        "date_data_generation": "test-experiment_nanopore-gregor",
        "sequencing_platform": "Oxford Nanopore PromethION 48",
        "chemistry_type": "R9.4.1",
        "was_barcoded": "TRUE",
        "barcode_kit": "test-experiment_nanopore-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("experiment_nanopore")
    return SampleValidator(
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_experiment_nanopore_valid_sample(get_validator, experiment_nanopore_sample):
    """Test that a valid experiment_nanopore sample passes validation"""
    validator = get_validator
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}


def test_experiment_nanopore_id_invalid_sample(  # in progress
    get_validator, experiment_nanopore_sample
):
    """Test that a sample with an invalid experiment_nanopore_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["experiment_nanopore_id"] = "TEST-TEST"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        "Value must start with BCM_"
    }  # wrong and current check_with needs to be changed


def test_analyte_id_invalid_sample(get_validator, experiment_nanopore_sample):
    """Test that a sample with an invalid analyte_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["analyte_id"] = "TEST-TEST"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        f"Value must start with BCM_Subject_ and end with _1_test-batch_id, _2_test-batch_id, _3_test-batch_id, or _4_test-batch_id",
    }


def test_experiment_type_normalization(get_validator, experiment_nanopore_sample):
    """Test that a sample's experiment_type properly normalizes with coerce: lowercase"""
    validator = get_validator
    experiment_nanopore_sample["experiment_type"] = "TARGETED"
    validator.normalized(experiment_nanopore_sample)
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}


def test_date_data_generation_normalization(get_validator, experiment_nanopore_sample):
    """Test that a sample's date_data_generation properly normalizes with coerce: year_month_date"""
    validator = get_validator
    experiment_nanopore_sample["date_data_generation"] = "12-25-2023"
    validator.normalized(experiment_nanopore_sample)
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}


def test_was_barcoded_normalization(get_validator, experiment_nanopore_sample):
    """Test that a sample's was_barcoded properly normalizes with coerce: uppercase"""
    validator = get_validator
    experiment_nanopore_sample["was_barcoded"] = "true"
    validator.normalized(experiment_nanopore_sample)
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}
