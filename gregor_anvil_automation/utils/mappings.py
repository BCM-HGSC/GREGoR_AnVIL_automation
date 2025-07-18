"""Various mappings used throughout the application"""

###################
# HEADER MAPPINGS #
###################

HEADER_CASE_SENSITIVE_MAP = {
    "genetic_findings": {
        "clingen_allele_id": "ClinGen_allele_ID",
        "gregor_variant_classification": "GREGoR_variant_classification",
        "gregor_clinvar_scv": "GREGoR_ClinVar_SCV",
        "public_database_id_other": "public_database_ID_other",
    }
}


CAN_NOT_BE_NA = {
    "aligned_dna_short_read_index_file",
    "aligned_dna_short_read_file",
    "aligned_nanopore_index_file",
    "aligned_nanopore_file",
}

################################
# CONDITIONALLY REQUIRED FIELD #
################################

# Field that is conditionally required: (Field depended on required, value001, ...)
CONDITIONALLY_REQ_MAPPING = {
    "chrom": ("variant_type", "SNV", "INDEL", "RE"),
    "pos": ("variant_type", "SNV", "INDEL", "RE"),
    "ref": ("variant_type", "SNV", "INDEL", "RE"),
    "alt": ("variant_type", "SNV", "INDEL", "RE"),
    "gene_of_interest": ("variant_type", "SNV", "INDEL", "RE"),
    "known_condition_name": ("gene_known_for_phenotype", "Known"),
    "condition_id": ("gene_known_for_phenotype", "Known"),
    "condition_inheritance": ("gene_known_for_phenotype", "Known"),
    "gregor_variant_classification": ("gene_known_for_phenotype", "Known"),
    "gene_disease_validity": ("gene_known_for_phenotype", "Known"),
    "partial_contribution_explained": ("phenotype_contribution", "Partial"),
}

#########################
# HEADER VALUE MAPPINGS #
#########################

genetic_findings_condition_inheritance = {
    "Autosomal recessive",
    "Autosomal dominant",
    "X-linked",
    "Mitochondrial",
    "Y-linked",
    "Contiguous gene syndrome",
    "Somatic mosaicism",
    "Digenic",
    "Other",
}

genetic_findings_method_of_discovery = {
    "SR-ES",
    "SR-GS",
    "LR-GS",
    "SNP array",
    "Optical mapping",
    "Karyotype",
    "SR RNA-seq",
    "LR RNA-seq",
    "SR-ES-reanalysis",
    "SR-GS-reanalysis",
    "LR-GS-reanalysis",
    "SNP array-reanalysis",
    "Optical mapping-reanalysis",
    "Karyotype-reanalysis",
    "SR RNA-seq-reanalysis",
    "LR RNA-seq-reanalysis",
}

participant_reported_race = {
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Native Hawaiian or Other Pacific Islander",
    "Middle Eastern or North African",
    "White",
}

phenotype_additional_modifiers = {
    "HP:0025292",
    "HP:0011009",
    "HP:0025308",
    "HP:0025307",
    "HP:0025306",
    "HP:0003581",
    "HP:0011420",
    "HP:0003831",
    "HP:0025285",
    "HP:0032525",
    "HP:0025286",
    "HP:0025254",
    "HP:0032526",
    "HP:0025257",
    "HP:0032503",
    "HP:0025256",
    "HP:0032522",
    "HP:0025255",
    "HP:0030674",
    "HP:0033820",
    "HP:4000052",
    "HP:0025287",
    "HP:0012832",
    "HP:0012827",
    "HP:0033815",
    "HP:0030645",
    "HP:0033816",
    "HP:0032535",
    "HP:0011463",
    "HP:0011010",
    "HP:0031797",
    "HP:0045088",
    "HP:4000051",
    "HP:4000048",
    "HP:4000047",
    "HP:0003577",
    "HP:0011421",
    "HP:0033763",
    "HP:0003819",
    "HP:0100613",
    "HP:0001522",
    "HP:0033765",
    "HP:0033764",
    "HP:0025294",
    "HP:0020034",
    "HP:4000053",
    "HP:0012839",
    "HP:0045089",
    "HP:0025293",
    "HP:0025302",
    "HP:0025282",
    "HP:0025708",
    "HP:0011460",
    "HP:0025303",
    "HP:0032365",
    "HP:0032502",
    "HP:0032501",
    "HP:0025315",
    "HP:0032534",
    "HP:0032542",
    "HP:0032500",
    "HP:0011461",
    "HP:0031914",
    "HP:0030650",
    "HP:4000042",
    "HP:0012837",
    "HP:4000043",
    "HP:0025295",
    "HP:0003829",
    "HP:0003593",
    "HP:0003587",
    "HP:0025709",
    "HP:0032539",
    "HP:0032540",
    "HP:0003621",
    "HP:0034199",
    "HP:0003584",
    "HP:0025710",
    "HP:0025275",
    "HP:0012831",
    "HP:0012835",
    "HP:0012838",
    "HP:0025291",
    "HP:0003596",
    "HP:0030648",
    "HP:0025279",
    "HP:0012825",
    "HP:0033817",
    "HP:0045090",
    "HP:0005268",
    "HP:0012826",
    "HP:0025296",
    "HP:0040006",
    "HP:0030651",
    "HP:0003811",
    "HP:0003623",
    "HP:0025301",
    "HP:0003680",
    "HP:4000046",
    "HP:0003674",
    "HP:4000050",
    "HP:0003679",
    "HP:0025280",
    "HP:0030647",
    "HP:0033814",
    "HP:0410280",
    "HP:0030649",
    "HP:0033813",
    "HP:0033819",
    "HP:0025304",
    "HP:0030646",
    "HP:0003812",
    "HP:0031450",
    "HP:0012830",
    "HP:0032544",
    "HP:0034241",
    "HP:0012829",
    "HP:0003676",
    "HP:0025297",
    "HP:0012840",
    "HP:4000040",
    "HP:0025305",
    "HP:0003678",
    "HP:0031796",
    "HP:0031375",
    "HP:0033818",
    "HP:0012834",
    "HP:0034198",
    "HP:4000049",
    "HP:0033349",
    "HP:0012828",
    "HP:0012824",
    "HP:0025281",
    "HP:0025284",
    "HP:0003677",
    "HP:0012836",
    "HP:4000045",
    "HP:0031915",
    "HP:0003826",
    "HP:0011011",
    "HP:0011008",
    "HP:0025283",
    "HP:0034197",
    "HP:0025153",
    "HP:4000044",
    "HP:0025204",
    "HP:0033185",
    "HP:0033032",
    "HP:0500261",
    "HP:0025205",
    "HP:0025208",
    "HP:0033789",
    "HP:0025206",
    "HP:0025207",
    "HP:0025334",
    "HP:0025211",
    "HP:0025227",
    "HP:0025377",
    "HP:0025212",
    "HP:0034060",
    "HP:0025215",
    "HP:0033793",
    "HP:0025209",
    "HP:0025213",
    "HP:0025210",
    "HP:0500260",
    "HP:0025214",
    "HP:0025216",
    "HP:0025217",
    "HP:0025218",
    "HP:0033184",
    "HP:0031167",
    "HP:0025220",
    "HP:0034195",
    "HP:0031135",
    "HP:0025221",
    "HP:0025222",
    "HP:0025223",
    "HP:0025224",
    "HP:0025225",
    "HP:0025226",
    "HP:0025228",
    "HP:0025219",
    "HP:0025229",
    "HP:0033198",
    "HP:0012833",
    "HP:0025290",
    "HP:0003828",
    "HP:0003682",
    "HP:0410401",
    "HP:0011462",
    "MONDO:0021125",
    "MONDO:0021135",
    "MONDO:0021139",
    "MONDO:0021149",
    "MONDO:0045034",
    "MONDO:0045040",
    "MONDO:0100355",
    "MONDO:0700004",
    "MONDO:0100369",
    "MONDO:0700061",
    "MONDO:0024488",
    "MONDO:0021126",
    "MONDO:0021136",
    "MONDO:0021137",
    "MONDO:0021140",
    "MONDO:0021141",
    "MONDO:0021151",
    "MONDO:0021152",
    "MONDO:0045036",
    "MONDO:0045035",
    "MONDO:0022202",
    "MONDO:0045042",
    "MONDO:0100356",
    "MONDO:0100357",
    "MONDO:0700005",
    "MONDO:0700006",
    "MONDO:0100427",
    "MONDO:0100426",
    "MONDO:0700063",
    "MONDO:0700062",
    "MONDO:0024489",
    "MONDO:0021128",
    "MONDO:0021127",
    "MONDO:0024497",
    "MONDO:0024495",
    "MONDO:0024490",
    "MONDO:0024496",
}

experiment_rna_short_read_experiment_type = {
    "single-end",
    "paired-end",
    "targeted",
    "untargeted",
}

experiment_rna_short_read_library_prep_type = {
    "stranded poly-A pulldown",
    "stranded total RNA",
    "rRNA depletion",
    "globin depletion",
}

MULTI_FIELD_MAP = {
    "condition_inheritance": genetic_findings_condition_inheritance,
    "reported_race": participant_reported_race,
    "additional_modifiers": phenotype_additional_modifiers,
    "method_of_discovery": genetic_findings_method_of_discovery,
    "experiment_type": experiment_rna_short_read_experiment_type,
    "library_prep_type": experiment_rna_short_read_library_prep_type,
}


#########
#########
TABLE_NAME_MAPPINGS = {
    "AlignedNanopore": "aligned_nanopore",
    "ExptNanopore": "experiment_nanopore",
    "AlignedShortRead": "aligned_dna_short_read",
    "ExpShortRead": "experiment_dna_short_read",
    "Genetic_Findings_Table": "genetic_findings",
}


UNIQUE_MAPPING = {
    "participant": ["participant_id"],
    "family": ["family_id"],
    "analyte": ["analyte_id"],
    "experiment_dna_short_read": ["experiment_dna_short_read_id"],
    "aligned_dna_short_read": [
        "aligned_dna_short_read_id",
        "experiment_dna_short_read_id",
    ],
    "experiment_nanopore": ["experiment_nanopore_id", "analyte_id"],
    "aligned_nanopore": ["aligned_nanopore_id", "experiment_nanopore_id"],
    "genetic_findings": ["genetic_findings_id"],
}

REFERENCE_SOURCE = {
    # source table : primary_key
    "analyte": "analyte_id",
    "experiment_dna_short_read": "experiment_dna_short_read_id",
    "experiment_rna_short_read": "experiment_rna_short_read_id",
    "experiment_nanopore": "experiment_nanopore_id",
    "family": "family_id",
    "participant": "participant_id",
    "phenotype": "term_id",
}


CROSS_REF_CHECK = [
    # table_name, source primary key, foreign key
    (
        "aligned_dna_short_read",
        "experiment_dna_short_read_id",
        "experiment_dna_short_read_id",
    ),
    (
        "aligned_rna_short_read",
        "experiment_rna_short_read_id",
        "experiment_rna_short_read_id",
    ),
    ("aligned_nanopore", "experiment_nanopore_id", "experiment_nanopore_id"),
    ("analyte", "participant_id", "participant_id"),
    ("experiment_dna_short_read", "analyte_id", "analyte_id"),
    ("experiment_rna_short_read_id", "analyte_id", "analyte_id"),
    ("experiment_nanopore", "analyte_id", "analyte_id"),
    ("genetic_findings", "participant_id", "participant_id"),
    (
        "genetic_findings",
        "participant_id",
        "additional_family_members_with_variant",
    ),
    ("genetic_findings", "term_id", "partial_contribution_explained"),
    ("participant", "family_id", "family_id"),
    ("participant", "participant_id", "twin_id"),
    ("phenotype", "participant_id", "participant_id"),
]
