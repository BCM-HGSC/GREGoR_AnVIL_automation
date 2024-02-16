import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="analyte_sample", scope="function")
def fixture_analyte_sample():
    return {
        "analyte_id": "BCM_Subject_TEST_1_A1",
        "participant_id": "BCM_Subject_TEST_1",
        "analyte_type": "DNA",
        "analyte_processing_details": "test-analyte-gregor",
        "primary_biosample": "UBERON:0000479",
        "primary_biosample_id": "test-analyte-gregor",
        "primary_biosample_details": "test-analyte-gregor",
        "tissue_affected_status": "Yes",
        "age_at_collection": "NA",
        "participant_drugs_intake": "test-analyte-gregor",
        "participant_special_diet": "test-analyte-gregor",
        "hours_since_last_meal": "test-analyte-gregor",
        "passage_number": "NA",
        "time_to_freeze": "NA",
        "sample_transformation_detail": "test-analyte-gregor",
        "quality_issues": "test-analyte-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("analyte")
    return SampleValidator(
        schema=schema, batch_number=1, gcp_bucket="test-gcp-bucket"
    )


def test_analyte_valid_sample(get_validator, analyte_sample):
    """Test that a valid analyte sample passes validation"""
    validator = get_validator
    validator.validate(analyte_sample)
    assert validator.errors == {}


def test_analyte_id_invalid_sample(get_validator, analyte_sample):
    """Test that a sample with an invalid analyte_id fails validation"""
    validator = get_validator
    analyte_sample["analyte_id"] = "TEST-TEST"
    participant_id = analyte_sample["participant_id"]
    validator.validate(analyte_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with {participant_id}_A and end with a number between 1 and 1, inclusively",
            f"Value must start with BCM_Subject_ and ends with _1_A, _2_A, _3_A, or _4_A and then a number between 1 and 1, inclusively",
        ],
    }


def test_participant_id_invalid_sample(get_validator, analyte_sample):
    """Test that a sample with an invalid participant_id fails validation"""
    validator = get_validator
    analyte_sample["participant_id"] = "TEST-TEST"
    participant_id = analyte_sample["participant_id"]
    validator.validate(analyte_sample)
    assert validator.errors == {
        "analyte_id": [f"Value must start with {participant_id}_A and end with a number between 1 and 1, inclusively"],
        "participant_id": ["Value must start with BCM_Subject"],
    }


def test_age_at_collection_invalid_sample(get_validator, analyte_sample):
    """Test that a sample with an invalid age_at_collection fails validation"""
    validator = get_validator
    analyte_sample["age_at_collection"] = "TEST-TEST"
    validator.validate(analyte_sample)
    assert validator.errors == {"age_at_collection": ["Value must be NA or an int"]}


def test_age_at_collection_is_int_valid_sample(get_validator, analyte_sample):
    """Test that a sample with a age_at_collection with a string number passes validation"""
    validator = get_validator
    analyte_sample["age_at_collection"] = "12345"
    validator.validate(analyte_sample)
    assert validator.errors == {}


def test_passage_number_invalid_sample(get_validator, analyte_sample):
    """Test that a sample with an invalid passage_number fails validation"""
    validator = get_validator
    analyte_sample["passage_number"] = "TEST-TEST"
    validator.validate(analyte_sample)
    assert validator.errors == {"passage_number": ["Value must be NA or an int"]}


def test_passage_number_is_int_valid_sample(get_validator, analyte_sample):
    """Test that a sample with a passage_number with a string number passes validation"""
    validator = get_validator
    analyte_sample["passage_number"] = "12345"
    validator.validate(analyte_sample)
    assert validator.errors == {}


def test_time_to_freeze_invalid_sample(get_validator, analyte_sample):
    """Test that a sample with an invalid time_to_freeze fails validation"""
    validator = get_validator
    analyte_sample["time_to_freeze"] = "TEST-TEST"
    validator.validate(analyte_sample)
    assert validator.errors == {"time_to_freeze": ["Value must be NA or an int"]}


def test_time_to_freeze_is_int_valid_sample(get_validator, analyte_sample):
    """Test that a sample with a time_to_freeze with a string number passes validation"""
    validator = get_validator
    analyte_sample["time_to_freeze"] = "12345"
    validator.validate(analyte_sample)
    assert validator.errors == {}


def test_tissue_affected_status_normalization(get_validator, analyte_sample):
    """Test that a sample's tissue_affected_status properly normalizes with coerce: intialcase"""
    validator = get_validator
    analyte_sample["tissue_affected_status"] = "yes"
    validator.validate(analyte_sample)
    assert validator.errors == {}
    assert validator.document["tissue_affected_status"] == "Yes"
