import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="participant_sample", scope="function")
def fixture_participant_sample():
    return {
        "participant_id": "BCM_Subject_TEST_1",
        "internal_project_id": "test-participant-gregor",
        "gregor_center": "BCM",
        "consent_code": "GRU",
        "recontactable": "Yes",
        "prior_testing": "test-participant-gregor",
        "pmid_id": "test-participant-gregor",
        "family_id": "BCM_Fam_TEST",
        "paternal_id": "0",
        "maternal_id": "0",
        "twin_id": "NA",
        "proband_relationship": "Self",
        "proband_relationship_detail": "test-participant-gregor",
        "sex": "Female",
        "sex_detail": "test-participant-gregor",
        "reported_race": "American Indian or Alaska Native",
        "reported_ethnicity": "Hispanic or Latino",
        "ancestry_detail": "test-participant-gregor",
        "age_at_last_observation": "0",
        "affected_status": "Affected",
        "phenotype_description": "test-participant-gregor",
        "age_at_enrollment": "0",
        "solve_status": "Yes",
        "missing_variant_case": "Yes",
        "missing_variant_details": "test-participant-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("participant")
    return SampleValidator(
        schema=schema, batch_number="test-batch_number", gcp_bucket="test-gcp-bucket"
    )


def test_participant_valid_sample(get_validator, participant_sample):
    """Test that a valid participant sample passes validation"""
    validator = get_validator
    validator.validate(participant_sample)
    assert validator.errors == {}


def test_participant_id_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid participant_id fails validation"""
    validator = get_validator
    participant_sample["participant_id"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {
        "participant_id": [
            "Value must start with BCM_Subject and end with _{a number}",
        ]
    }


def test_family_id_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid family_id fails validation"""
    validator = get_validator
    participant_sample["family_id"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {"family_id": ["Value must start with BCM_Fam"]}


def test_paternal_id_valid_sample_non_zero(get_validator, participant_sample):
    """Test that a sample with an valid paternal_id passes validation"""
    validator = get_validator
    participant_sample["paternal_id"] = "BCM_Subject_TEST_3"
    validator.validate(participant_sample)
    assert validator.errors == {}


def test_paternal_id_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid paternal_id fails validation"""
    validator = get_validator
    participant_sample["paternal_id"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {
        "paternal_id": [
            "Value must be '0' or match the format of BCM_Subject_######_3, and match the subject id in `participant_id`"
        ]
    }


def test_paternal_id_invalid_sample_different_subject_id(
    get_validator, participant_sample
):
    """Test that a sample with an invalid paternal_id fails validation"""
    validator = get_validator
    participant_sample["paternal_id"] = "BCM_Subject_TEST-TEST_1"
    validator.validate(participant_sample)
    assert validator.errors == {
        "paternal_id": [
            "Value must be '0' or match the format of BCM_Subject_######_3, and match the subject id in `participant_id`",
        ],
    }


def test_maternal_id_valid_sample_non_zero(get_validator, participant_sample):
    """Test that a sample with an valid maternal_id passes validation"""
    validator = get_validator
    participant_sample["maternal_id"] = "BCM_Subject_TEST_2"
    validator.validate(participant_sample)
    assert validator.errors == {}


def test_maternal_id_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid maternal_id fails validation"""
    validator = get_validator
    participant_sample["maternal_id"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {
        "maternal_id": [
            "Value must be '0' or match the format of BCM_Subject_######_2, and match the subject id in `participant_id`"
        ]
    }


def test_maternal_id_invalid_sample_different_subject_id(
    get_validator, participant_sample
):
    """Test that a sample with an invalid maternal_id fails validation"""
    validator = get_validator
    participant_sample["maternal_id"] = "BCM_Subject_TEST-TEST_1"
    validator.validate(participant_sample)
    assert validator.errors == {
        "maternal_id": [
            "Value must be '0' or match the format of BCM_Subject_######_2, and match the subject id in `participant_id`",
        ],
    }


def test_twin_id_no_two_ids_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid twin_id fails validation"""
    validator = get_validator
    participant_sample["twin_id"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {"twin_id": ["Value does not contain `participant_id`"]}


def test_twin_id_no_two_ids_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid twin_id fails validation"""
    validator = get_validator
    participant_sample["twin_id"] = "BCM_Subject_TEST_1"
    validator.validate(participant_sample)
    assert validator.errors == {"twin_id": ["Value does not have exactly two ids"]}


def test_twin_id_no_matching_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid twin_id fails validation"""
    validator = get_validator
    participant_sample["twin_id"] = "BCM_Subject_TEST-TEST_1 BCM_Subject_TEST_4"
    participant_sample["participant_id"] = "BCM_Subject_TEST-TEST_1"
    participant_id = participant_sample["participant_id"]
    subject_id = participant_id.split("_")[2]
    matching = (
        f"BCM_Subject_{subject_id}_{'4' if participant_id.endswith('_1') else '1'}"
    )
    validator.validate(participant_sample)
    assert validator.errors == {
        "twin_id": [f"Twin id does not match expected format of: {matching}"]
    }


def test_age_at_last_observation_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid age_at_last_observation fails validation"""
    validator = get_validator
    participant_sample["age_at_last_observation"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {
        "age_at_last_observation": ["Value must be NA or an int"]
    }


def test_age_at_last_observation_is_int_valid_sample(get_validator, participant_sample):
    """Test that a sample with a age_at_last_observation with a string number passes validation"""
    validator = get_validator
    participant_sample["age_at_last_observation"] = "12345"
    validator.validate(participant_sample)
    assert validator.errors == {}


def test_age_at_enrollment_invalid_sample(get_validator, participant_sample):
    """Test that a sample with an invalid age_at_enrollment fails validation"""
    validator = get_validator
    participant_sample["age_at_enrollment"] = "TEST-TEST"
    validator.validate(participant_sample)
    assert validator.errors == {"age_at_enrollment": ["Value must be NA or an int"]}


def test_age_at_enrollment_is_int_valid_sample(get_validator, participant_sample):
    """Test that a sample with a age_at_enrollment with a string number passes validation"""
    validator = get_validator
    participant_sample["age_at_enrollment"] = "12345"
    validator.validate(participant_sample)
    assert validator.errors == {}


def test_gregor_center_normalization(get_validator, participant_sample):
    """Test that a sample's gregor_center properly normalizes with coerce: uppercase"""
    validator = get_validator
    participant_sample["gregor_center"] = "bcm"
    validator.validate(participant_sample)
    assert validator.errors == {}
    assert validator.document["gregor_center"] == "BCM"


def test_recontactable_normalization(get_validator, participant_sample):
    """Test that a sample's recontactable properly normalizes with coerce: initialcase"""
    validator = get_validator
    participant_sample["recontactable"] = "yes"
    validator.validate(participant_sample)
    assert validator.errors == {}
    assert validator.document["recontactable"] == "Yes"


def test_proband_relationship_normalization(get_validator, participant_sample):
    """Test that a sample's proband_relationship properly normalizes with coerce: titlecase"""
    validator = get_validator
    participant_sample["proband_relationship"] = "maternal half sibling"
    validator.validate(participant_sample)
    assert validator.errors == {}
    assert validator.document["proband_relationship"] == "Maternal Half Sibling"


def test_sex_normalization(get_validator, participant_sample):
    """Test that a sample's sex properly normalizes with coerce: initialcase"""
    validator = get_validator
    participant_sample["sex"] = "female"
    validator.validate(participant_sample)
    assert validator.errors == {}
    assert validator.document["sex"] == "Female"


def test_solve_status_normalization(get_validator, participant_sample):
    """Test that a sample's solve_status properly normalizes with coerce: initialcase"""
    validator = get_validator
    participant_sample["solve_status"] = "yes"
    validator.validate(participant_sample)
    assert validator.errors == {}
    assert validator.document["solve_status"] == "Yes"


def test_missing_variant_case_normalization(get_validator, participant_sample):
    """Test that a sample's missing_variant_case properly normalizes with coerce: initialcase"""
    validator = get_validator
    participant_sample["missing_variant_case"] = "yes"
    validator.validate(participant_sample)
    assert validator.errors == {}
    assert validator.document["missing_variant_case"] == "Yes"
