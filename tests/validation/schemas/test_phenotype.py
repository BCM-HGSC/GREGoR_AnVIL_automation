import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="phenotype_sample", scope="function")
def fixture_phenotype_sample():
    return {
        "phenotype_id": "test-phenotype-gregor",
        "participant_id": "BCM_Subject_TEST_1",
        "term_id": "HP:TEST",
        "presence": "Present",
        "ontology": "HPO",
        "additional_details": "test-phenotype-gregor",
        "onset_age_range": "HP:0003581",
        "additional_modifiers": "HP:0025292",
        "syndromic": "syndromic",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("phenotype")
    return SampleValidator(
        schema=schema, batch_number="test-batch_number", gcp_bucket="test-gcp-bucket"
    )


def test_phenotype_valid_sample(get_validator, phenotype_sample):
    """Test that a valid phenotype sample passes validation"""
    validator = get_validator
    validator.validate(phenotype_sample)
    assert validator.errors == {}


def test_participant_id_invalid_sample(get_validator, phenotype_sample):
    """Test that a sample with an invalid participant_id fails validation"""
    validator = get_validator
    phenotype_sample["participant_id"] = "TEST-TEST"
    validator.validate(phenotype_sample)
    assert validator.errors == {
        "participant_id": [
            "Value must start with BCM_Subject and end with _{a number}",
        ]
    }


def test_term_id_invalid_sample(get_validator, phenotype_sample):
    """Test that a sample with an invalid term_id fails validation"""
    validator = get_validator
    phenotype_sample["term_id"] = "TEST-TEST"
    validator.validate(phenotype_sample)
    assert validator.errors == {"term_id": ["Value must start with HP: or MONDO:"]}


def test_presence_normalization(get_validator, phenotype_sample):
    """Test that a sample's presence properly normalizes with coerce: initialcase"""
    validator = get_validator
    phenotype_sample["presence"] = "present"
    validator.validate(phenotype_sample)
    assert validator.errors == {}
    assert validator.document["presence"] == "Present"


def test_ontology_normalization(get_validator, phenotype_sample):
    """Test that a sample's ontology properly normalizes with coerce: uppercase"""
    validator = get_validator
    phenotype_sample["ontology"] = "hpo"
    validator.validate(phenotype_sample)
    assert validator.errors == {}
    assert validator.document["ontology"] == "HPO"


def test_syndromic_normalization(get_validator, phenotype_sample):
    """Test that a sample's syndromic properly normalizes with coerce: lowercase"""
    validator = get_validator
    phenotype_sample["syndromic"] = "SYNDROMIC"
    validator.validate(phenotype_sample)
    assert validator.errors == {}
    assert validator.document["syndromic"] == "syndromic"


def test_additional_modifiers(get_validator, phenotype_sample):
    """Verifies that sample's `additional_modifiers` is correctly validated"""
    validator = get_validator
    phenotype_sample["additional_modifiers"] = "TEST"
    validator.validate(phenotype_sample)
    assert validator.errors == {
        "additional_modifiers": ["Values ({'TEST'}) are not accepted"]
    }
    phenotype_sample["additional_modifiers"] = "HP:0011009 | MONDO:0024490"
    validator.validate(phenotype_sample)
    assert validator.errors == {}
    phenotype_sample["additional_modifiers"] = "TEST | MONDO:0024490"
    validator.validate(phenotype_sample)
    assert validator.errors == {
        "additional_modifiers": ["Values ({'TEST'}) are not accepted"]
    }
