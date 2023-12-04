import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="analyte_sample", scope="function")
def fixture_analyte_sample():
    return {
        "analyte_id": "BCM_SUBJECT_TEST_1_test-batch_id",
        "participant_id": "BCM_SUBJECT_TEST_1",
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
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_analyte_valid_sample(get_validator, analyte_sample):
    """Test that a valid analyte sample passes validation"""
    validator = get_validator
    validator.validate(analyte_sample)
    assert validator.errors == {}


def test_analyte_id_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid analyte_id fails validation"""
    validator = get_validator
    aligned_nanopore_sample["analyte_id"] = "TEST-TEST"
    participant_id = aligned_nanopore_sample["participant_id"]
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {
        f"Value must match the format of {participant_id}_test-batch_id",
        f"Value must start with BCM_Subject_ and end with _1_test-batch_id, _2_test-batch_id, _3_test-batch_id, or _4_test-batch_id",
    }


def test_participant_id_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid participant_id fails validation"""
    validator = get_validator
    aligned_nanopore_sample["participant_id"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {
        "Value must start with BCM_Subject and end with either _1, _2, _3, or _4"
    }


def test_age_at_collection_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid age_at_collection fails validation"""
    validator = get_validator
    aligned_nanopore_sample["age_at_collection"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"Value must be NA or an int"}


def test_passage_number_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid passage_number fails validation"""
    validator = get_validator
    aligned_nanopore_sample["passage_number"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"Value must be NA or an int"}


def test_time_to_freeze_invalid_sample(get_validator, aligned_nanopore_sample):
    """Test that a sample with an invalid time_to_freeze fails validation"""
    validator = get_validator
    aligned_nanopore_sample["time_to_freeze"] = "TEST-TEST"
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {"Value must be NA or an int"}


def test_sex_tissue_affected_status_normalization(
    get_validator, aligned_nanopore_sample
):
    """Test that a sample's tissue_affected_status properly normalizes with coerce: intialcase"""
    validator = get_validator
    aligned_nanopore_sample["tissue_affected_status"] = "yes"
    validator.normalized(aligned_nanopore_sample)
    validator.validate(aligned_nanopore_sample)
    assert validator.errors == {}
