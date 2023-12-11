import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="family_sample", scope="function")
def fixture_family_sample():
    return {
        "family_id": "BCM_Fam_BHTEST",
        "consanguinity": "None suspected",
        "consanguinity_detail": "test-family-gregor",
        "family_history_detail": "test-family-gregor",
        "pedigree_file": "test-family-gregor",
        "pedigree_file_detail": "test-family-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("family")
    return SampleValidator(
        schema=schema, batch_id="test-batch_id", gcp_bucket="test-gcp-bucket"
    )


def test_family_valid_sample(get_validator, family_sample):
    """Test that a valid family sample passes validation"""
    validator = get_validator
    validator.validate(family_sample)
    assert validator.errors == {}


def test_family_invalid_family_id(get_validator, family_sample):
    """Test that a sample with a valid famil_id passes validation"""
    validator = get_validator
    family_sample["family_id"] = "TEST-TEST"
    validator.validate(family_sample)
    assert validator.errors == {"family_id": ["Value must start with BCM_Fam"]}


def test_family_consanguinity_titlecase(get_validator, family_sample):
    """Test that a sample's consanguinity properly normalizes with coerce: titlecase"""
    validator = get_validator
    family_sample["consanguinity"] = "none suspected"
    validator.validate(family_sample)
    assert validator.errors == {}
    assert validator.document["consanguinity"] == "None suspected"
