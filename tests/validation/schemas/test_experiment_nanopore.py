import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="experiment_nanopore_sample", scope="function")
def fixture_experiment_nanopore_sample():
    return {
        "experiment_nanopore_id": "BCM_ONTWGS_BHTEST_1",
        "analyte_id": "BCM_Subject_TEST_1_A1",
        "experiment_sample_id": "test-experiment_nanopore-gregor",
        "seq_library_prep_kit_method": "LSK109",
        "fragmentation_method": "test-experiment_nanopore-gregor",
        "experiment_type": "targeted",
        "targeted_regions_method": "test-experiment_nanopore-gregor",
        "targeted_region_bed_file": "test-experiment_nanopore-gregor",
        "date_data_generation": "2023-12-25",
        "sequencing_platform": "Oxford Nanopore PromethION 48",
        "chemistry_type": "R9.4.1",
        "was_barcoded": "TRUE",
        "barcode_kit": "test-experiment_nanopore-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("experiment_nanopore")
    return SampleValidator(schema=schema, batch_number=1, gcp_bucket="test-gcp-bucket")


def test_experiment_nanopore_valid_sample(get_validator, experiment_nanopore_sample):
    """Test that a valid experiment_nanopore sample passes validation"""
    validator = get_validator
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}


def test_experiment_nanopore_id_invalid_sample(
    get_validator, experiment_nanopore_sample
):
    """Test that a sample with an invalid experiment_nanopore_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["experiment_nanopore_id"] = "TEST-TEST"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        "experiment_nanopore_id": [
            "Value must end with _{some_number}",
            "Value must start with BCM_ONTWGS_BH",
        ]
    }


def test_analyte_id_invalid_sample_no_passes(get_validator, experiment_nanopore_sample):
    """Test that a sample with an invalid analyte_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["analyte_id"] = "TEST-TEST"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with BCM_Subject_ and ends with _`a number`_A and then a number between 1 and 1, inclusively",
        ]
    }


def test_analyte_id_invalid_sample_no_start(get_validator, experiment_nanopore_sample):
    """Test that a sample with an invalid anlyte_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["analyte_id"] = "TEST-TEST_1_A1"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with BCM_Subject_ and ends with _`a number`_A and then a number between 1 and 1, inclusively",
        ]
    }


def test_analyte_id_invalid_sample_no_mid_num(
    get_validator, experiment_nanopore_sample
):
    """Test that a sample with an invalid anlyte_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["analyte_id"] = "BCM_Subject_TEST-TEST_A1"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with BCM_Subject_ and ends with _`a number`_A and then a number between 1 and 1, inclusively",
        ]
    }


def test_analyte_id_invalid_sample_no_end_num(
    get_validator, experiment_nanopore_sample
):
    """Test that a sample with an invalid anlyte_id fails validation"""
    validator = get_validator
    experiment_nanopore_sample["analyte_id"] = "BCM_Subject_TEST-TEST_1_A"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with BCM_Subject_ and ends with _`a number`_A and then a number between 1 and 1, inclusively",
        ]
    }


def test_experiment_type_normalization(get_validator, experiment_nanopore_sample):
    """Test that a sample's experiment_type properly normalizes with coerce: lowercase"""
    validator = get_validator
    experiment_nanopore_sample["experiment_type"] = "TARGETED"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["experiment_type"] == "targeted"


def test_date_data_generation_normalization(get_validator, experiment_nanopore_sample):
    """Test that a sample's date_data_generation properly normalizes with coerce: year_month_date"""
    validator = get_validator
    experiment_nanopore_sample["date_data_generation"] = "12-25-2023"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["date_data_generation"] == "2023-12-25"


def test_date_data_generation_normalization_farthest(
    get_validator, experiment_nanopore_sample
):
    """Test that a sample's date_data_generation properly normalizes with coerce: year_month_date"""
    validator = get_validator
    experiment_nanopore_sample["date_data_generation"] = "1/1/23"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["date_data_generation"] == "2023-01-01"


def test_date_data_generation_normalization_when_na(
    get_validator, experiment_nanopore_sample
):
    """Test that a sample's date_data_generation properly passes NA through with coerce: year_month_date"""
    validator = get_validator
    experiment_nanopore_sample["date_data_generation"] = "NA"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["date_data_generation"] == "NA"


def test_was_barcoded_normalization(get_validator, experiment_nanopore_sample):
    """Test that a sample's was_barcoded properly normalizes with coerce: uppercase"""
    validator = get_validator
    experiment_nanopore_sample["was_barcoded"] = "true"
    validator.validate(experiment_nanopore_sample)
    assert validator.errors == {}
    assert validator.document["was_barcoded"] == "TRUE"
