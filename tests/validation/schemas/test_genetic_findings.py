import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema


@pytest.fixture(name="genetic_findings_sample", scope="function")
def fixture_genetic_findings_sample():
    return {
        "genetic_findings_id": "test-genetic_findings-gregor",
        "participant_id": "BCM_Subject_BHTEST_1",
        "experiment_id": "test-genetic_findings-gregor",
        "variant_type": "SNV/INDEL",
        "variant_reference_assembly": "GRCh38",
        "chrom": "1",
        "pos": "256",
        "ref": "C",
        "alt": "T",
        "clingen_allele_id": "test-genetic_findings-gregor",
        "gene": "test-genetic_findings-gregor",
        "transcript": "test-genetic_findings-gregor",
        "hgvsc": "test-genetic_findings-gregor",
        "hgvsp": "test-genetic_findings-gregor",
        "zygosity": "Heterozygous",
        "allele_balance_or_heteroplasmy_percentage": "test-genetic_findings-gregor",
        "variant_inheritance": "de novo",
        "linked_variant": "test-genetic_findings-gregor",
        "linked_variant_phase": "in trans",
        "gene_known_for_phenotype": "Known",
        "known_condition_name": "test-genetic_findings-gregor",
        "condition_id": "test-genetic_findings-gregor",
        "condition_inheritance": "Autosomal recessive",
        "gregor_variant_classification": "Benign",
        "gregor_clinvar_scv": "test-genetic_findings-gregor",
        "public_database_other": "test-genetic_findings-gregor",
        "public_database_id_other": "test-genetic_findings-gregor",
        "phenotype_contribution": "Partial",
        "partial_contribution_explained": "test-genetic_findings-gregor",
        "additional_family_members_with_variant": "test-genetic_findings-gregor",
        "method_of_discovery": "SR-ES",
        "notes": "test-genetic_findings-gregor",
    }


@pytest.fixture(name="get_validator")
def fixture_get_validator():
    schema = get_schema("genetic_findings")
    return SampleValidator(
        schema=schema, batch_number="test-batch_number", gcp_bucket="test-gcp-bucket"
    )


def test_genetic_findings_valid_sample(get_validator, genetic_findings_sample):
    """Test that a valid genetic_findings sample passes validation"""
    validator = get_validator
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_participant_id_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid participant_id fails validation"""
    validator = get_validator
    genetic_findings_sample["participant_id"] = "TEST-TEST"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "participant_id": [
            "Value must start with BCM_Subject and end with _{a number}",
        ],
    }


def test_participant_id_invalid_sample_different_subject_id(
    get_validator, genetic_findings_sample
):
    """Test that a sample with an invalid participant_id fails validation"""
    validator = get_validator
    genetic_findings_sample["participant_id"] = "BCM_Subject_TEST-TEST_1"
    participant_id = genetic_findings_sample["participant_id"]
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "analyte_id": [
            f"Value must start with {participant_id}_A and end with a number between 1 and 1, inclusively"
        ],
        "participant_id": [
            "Value must start with BCM_Subject and end with _{a number}",
        ],
    }


def test_pos_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid pos fails validation"""
    validator = get_validator
    genetic_findings_sample["pos"] = "TEST-TEST"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "pos": [
            "Value requires an int",
        ],
    }


def test_variant_type_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's variant_type properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["variant_type"] = "snv/indel"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["variant_type"] == "SNV/INDEL"


def test_chrom_type_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's chrom properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["chrom"] = "mt"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["chrom"] == "MT"


def test_ref_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's ref properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["ref"] = "c"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["ref"] == "C"


def test_alt_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's alt properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["alt"] = "t"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["alt"] == "T"


def test_zygosity_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's zygosity properly normalizes with coerce: initialcase"""
    validator = get_validator
    genetic_findings_sample["zygosity"] = "heterozygous"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["zygosity"] == "Heterozygous"


def test_variant_inheritance_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's variant_inheritance properly normalizes with coerce: lowercase"""
    validator = get_validator
    genetic_findings_sample["variant_inheritance"] = "DE NOVO"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["variant_inheritance"] == "de novo"


def test_linked_variant_phase_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's linked_variant_phase properly normalizes with coerce: lowercase"""
    validator = get_validator
    genetic_findings_sample["linked_variant_phase"] = "IN TRANS"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["linked_variant_phase"] == "in trans"


def test_gene_known_for_phenotype_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's gene_known_for_phenotype properly normalizes with coerce: initialcase"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "known"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["gene_known_for_phenotype"] == "Known"


def test_condition_inheritance_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's condition_inheritance properly normalizes with coerce: initialcase"""
    validator = get_validator
    genetic_findings_sample["condition_inheritance"] = "autosomal recessive"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["condition_inheritance"] == "Autosomal recessive"


def test_phenotype_contribution_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's phenotype_contribution properly normalizes with coerce: initialcase"""
    validator = get_validator
    genetic_findings_sample["phenotype_contribution"] = "partial"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["phenotype_contribution"] == "Partial"
