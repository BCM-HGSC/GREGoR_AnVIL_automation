import pytest
from pathlib import Path

from gregor_anvil_automation.validation.sample import SampleValidator
from gregor_anvil_automation.validation.schema import get_schema
from gregor_anvil_automation.utils.mappings import MULTI_FIELD_MAP


@pytest.fixture(name="genetic_findings_sample", scope="function")
def fixture_genetic_findings_sample():
    return {
        "genetic_findings_id": "test-genetic_findings-gregor",
        "participant_id": "BCM_Subject_BHTEST_1",
        "experiment_id": "test-genetic_findings-gregor",
        "variant_type": "SNV/INDEL",
        "sv_type": "BND",
        "variant_reference_assembly": "GRCh38",
        "chrom": "1",
        "chrom_end": "2",
        "pos": "256",
        "pos_end": "512",
        "ref": "C",
        "alt": "T",
        "copy_number": "1",
        "clingen_allele_id": "test-genetic_findings-gregor",
        "gene_of_interest": "intergenic",
        "transcript": "test-genetic_findings-gregor",
        "hgvsc": "test-genetic_findings-gregor",
        "hgvsp": "test-genetic_findings-gregor",
        "hgvs": "test-genetic_findings-gregor",
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
        "gene_disease_validity": "Definitive",
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


def test_chrom_valid_sample_snv_indel(get_validator, genetic_findings_sample):
    """Test that a sample with a valid chrom passes validation"""
    validator = get_validator
    genetic_findings_sample["chrom"] = "1"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_chrom_valid_sample_re(get_validator, genetic_findings_sample):
    """Test that a sample with a valid chrom passes validation"""
    validator = get_validator
    genetic_findings_sample["chrom"] = "1"
    genetic_findings_sample["variant_type"] = "RE"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_chrom_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid chrom fails validation"""
    validator = get_validator
    genetic_findings_sample["chrom"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "chrom": [
            "Value may only exist if variant_type is SNV/INDEL or RE",
        ],
    }


def test_pos_valid_sample_is_int_snv_indel(get_validator, genetic_findings_sample):
    """Test that a sample with a valid pos passes validation"""
    validator = get_validator
    genetic_findings_sample["pos"] = "1"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_pos_valid_sample_is_int_sample_re(get_validator, genetic_findings_sample):
    """Test that a sample with a valid pos passes validation"""
    validator = get_validator
    genetic_findings_sample["pos"] = "1"
    genetic_findings_sample["variant_type"] = "RE"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_pos_invalid_sample_is_int_wrong_variant_type(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid pos fails validation"""
    validator = get_validator
    genetic_findings_sample["pos"] = "1"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "pos": [
            "Value may only exist if variant_type is SNV/INDEL or RE",
        ],
    }

def test_pos_invalid_sample_not_int_right_variant_type(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid pos fails validation"""
    validator = get_validator
    genetic_findings_sample["pos"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "pos": [
            "Value requires an int",
        ],
    }


def test_pos_invalid_sample_not_int_wrong_variant_type(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid pos fails validation"""
    validator = get_validator
    genetic_findings_sample["pos"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "pos": [
            "Value requires an int",
            "Value may only exist if variant_type is SNV/INDEL or RE",
        ],
    }


def test_pos_end_valid_sample_is_int(get_validator, genetic_findings_sample):
    """Test that a sample with an valid pos_end passes validation"""
    validator = get_validator
    genetic_findings_sample["pos_end"] = "1"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_pos_end_invalid_sample_not_int(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid pos_end fails validation"""
    validator = get_validator
    genetic_findings_sample["pos_end"] = "TEST-TEST"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "pos_end": [
            "Value requires an int",
        ],
    }


def test_ref_valid_sample_snv_indel(get_validator, genetic_findings_sample):
    """Test that a sample with a valid ref passes validation"""
    validator = get_validator
    genetic_findings_sample["ref"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_ref_valid_sample_re(get_validator, genetic_findings_sample):
    """Test that a sample with a valid ref passes validation"""
    validator = get_validator
    genetic_findings_sample["ref"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "RE"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_ref_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid ref fails validation"""
    validator = get_validator
    genetic_findings_sample["ref"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "ref": [
            "Value may only exist if variant_type is SNV/INDEL or RE",
        ],
    }


def test_alt_valid_sample_snv_indel(get_validator, genetic_findings_sample):
    """Test that a sample with a valid alt passes validation"""
    validator = get_validator
    genetic_findings_sample["alt"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_alt_valid_sample_re(get_validator, genetic_findings_sample):
    """Test that a sample with a valid alt passes validation"""
    validator = get_validator
    genetic_findings_sample["alt"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "RE"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_alt_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid alt fails validation"""
    validator = get_validator
    genetic_findings_sample["alt"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "alt": [
            "Value may only exist if variant_type is SNV/INDEL or RE",
        ],
    }


# TODO: Replace all gene_of_interest check_with tests with new ones in accordance with check_with changes
def test_gene_of_interest_valid_sample_snv_indel(get_validator, genetic_findings_sample):
    """Test that a sample with a valid gene_of_interest passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "intergenic"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gene_of_interest_valid_sample_re(get_validator, genetic_findings_sample):
    """Test that a sample with a valid gene_of_interest passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "intergenic"
    genetic_findings_sample["variant_type"] = "RE"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gene_of_interest_valid_sample_empty(get_validator, genetic_findings_sample):
    """Test that a sample with a valid gene_of_interest passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = ""
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gene_of_interest_invalid_sample_not_intergenic_snv_indel(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid gene_of_interest fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "SNV/INDEL"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "gene_of_interest": [
            "Value must be 'intergenic' if variant_type is SNV/INDEL or RE is intergenic with no clear gene of interest",
        ],
    }


def test_gene_of_interest_invalid_sample_not_intergenic_re(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid gene_of_interest fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "RE"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "gene_of_interest": [
            "Value must be 'intergenic' if variant_type is SNV/INDEL or RE is intergenic with no clear gene of interest",
        ],
    }


def test_gene_of_interest_invalid_sample_intergenic_wrong_variant_type(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid gene_of_interest fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "intergenic"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "gene_of_interest": [
            "Value may only be 'intergenic' if variant_type is SNV/INDEL or RE",
        ],
    }


def test_gene_of_interest_invalid_sample_not_empty(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid gene_of_interest fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "TEST-TEST"
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "gene_of_interest": [
            "Value must be empty if SV has no specific gene of interest",
        ],
    }


def test_known_condition_name_valid_na(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a known_condition_name of 'NA' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Candidate"
    genetic_findings_sample["known_condition_name"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_known_condition_name_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid known_condition_name fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["known_condition_name"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "known_condition_name": [
            "Value may only be NA if gene_known_for_phenotype is not Known"
        ],
    }


def test_condition_id_valid_na(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a condition_id of 'NA' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Candidate"
    genetic_findings_sample["condition_id"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_condition_id_invalid_sample(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid condition_id fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["condition_id"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "condition_id": [
            "Value may only be NA if gene_known_for_phenotype is not Known"
        ],
    }


def test_condition_inheritance_valid_single_value_and_known(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a condition_inheritance of 'NA' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["condition_inheritance"] = "Autosomal recessive"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_condition_inheritance_valid_multi_value_and_known(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a condition_inheritance of 'NA' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["condition_inheritance"] = "Autosomal recessive|Autosomal dominant|X-linked"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_condition_inheritance_valid_na_and_not_known(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a condition_inheritance of 'NA' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Candidate"
    genetic_findings_sample["condition_inheritance"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_condition_inheritance_invalid_sample_na_and_known(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid condition_inheritance fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["condition_inheritance"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "condition_inheritance": [
            "Value is required if gene_known_for_phenotype is Known"
        ],
    }


def test_condition_inheritance_invalid_sample_invalid_value_and_known(get_validator, genetic_findings_sample):
    """Test that a sample with an invalid condition_inheritance fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["condition_inheritance"] = "TEST-TEST"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "condition_inheritance": [
            f"Values ({genetic_findings_sample["gene_known_for_phenotype"]}) are not accepted"
        ],
    }


def test_gregor_variant_classification_valid_na(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a gregor_variant_classification of 'NA' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Candidate"
    genetic_findings_sample["gregor_variant_classification"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gregor_variant_classification_invalid_sample(
    get_validator, genetic_findings_sample
):
    """Test that a sample with an invalid gregor_variant_classification fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["gregor_variant_classification"] = "NA"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "gregor_variant_classification": [
            "Value may only be NA if gene_known_for_phenotype is not Known"
        ],
    }


def test_gene_disease_validity_valid_sample_not_known_and_not_empty(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and a gene_disease_validity of 'Definitive' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Candidate"
    genetic_findings_sample["gene_disease_validity"] = "Definitive"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gene_disease_validity_valid_sample_known_and_not_empty(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Known' and a gene_disease_validity of 'Definitive' passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["gene_disease_validity"] = "Definitive"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gene_disease_validity_valid_sample_not_known_and_empty(get_validator, genetic_findings_sample):
    """Test that a sample with a gene_known_for_phenotype of 'Candidate' and an empty gene_disease_validity passes validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Candidate"
    genetic_findings_sample["gene_disease_validity"] = ""
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_gene_disease_validity_invalid_sample_known_and_empty(
    get_validator, genetic_findings_sample
):
    """Test that a sample with an invalid gene_disease_validity fails validation"""
    validator = get_validator
    genetic_findings_sample["gene_known_for_phenotype"] = "Known"
    genetic_findings_sample["gene_disease_validity"] = ""
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "gene_disease_validity": [
            "Value is required if gene_known_for_phenotype is Known"
        ],
    }


def test_method_of_discovery_valid_sample(
    get_validator, genetic_findings_sample
):
    """Test that a sample with an invalid method_of_discovery passes validation"""
    validator = get_validator
    genetic_findings_sample["method_of_discovery"] = "SR-ES|SR-GS|LR-GS"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}


def test_method_of_discovery_invalid_sample(
    get_validator, genetic_findings_sample
):
    """Test that a sample with an invalid method_of_discovery passes validation"""
    validator = get_validator
    genetic_findings_sample["method_of_discovery"] = "SR-ES-SR-GS-LR-GS"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {
        "method_of_discovery": [
            f"Values ({genetic_findings_sample["method_of_discovery"]}) are not accepted"
        ],
    }


def test_variant_type_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's variant_type properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["variant_type"] = "snv/indel"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["variant_type"] == "SNV/INDEL"


def test_sv_type_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's sv_type properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["sv_type"] = "bnd"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["sv_type"] == "SNV/INDEL"


def test_chrom_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's chrom properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["chrom"] = "mt"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["chrom"] == "MT"


def test_chrom_end_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's chrom_end properly normalizes with coerce: uppercase"""
    validator = get_validator
    genetic_findings_sample["chrom_end"] = "mt"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["chrom_end"] == "MT"


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

# TODO: Replace all gene_of_interest normalization with new ones in accordance with check_with changes
def test_gene_of_interest_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's gene_of_interest properly normalizes with coerce: multi_with_additional_rules"""
    validator = get_validator
    genetic_findings_sample["gene_of_interest"] = "   TEST  | TEST  "
    genetic_findings_sample["variant_type"] = "CNV"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["gene_of_interest"] == "TEST|TEST"


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


def test_method_of_discovery_normalization(get_validator, genetic_findings_sample):
    """Test that a sample's method_of_discovery properly normalizes with coerce: multi"""
    validator = get_validator
    genetic_findings_sample["method_of_discovery"] = "   SR-ES  | SR_GS  |    LR-GS"
    validator.validate(genetic_findings_sample)
    assert validator.errors == {}
    assert validator.document["method_of_discovery"] == "SR-ES|SR-GS|LR-GS"