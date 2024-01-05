"""Various mappings used throughout the application"""

TABLE_NAME_MAPPINGS = {
    "AlignedNanopore": "aligned_nanopore",
    "ExptNanopore": "experiment_nanopore",
    "AlignedShortRead": "aligned_dna_short_read",
    "ExpShortRead": "experiment_dna_short_read",
}


UNIQUE_MAPPING = {
    "participant": {"participant_id"},
    "family": {"family_id"},
    "phenotype": {"participant_id"},
    "analyte": {"analyte_id", "participant_id"},
    "experiment_dna_short_read": {"analyte_id", "experiment_dna_short_read_id"},
    "aligned_dna_short_read": {
        "aligned_dna_short_read_id",
        "experiment_dna_short_read_id",
    },
    "experiment_nanopore": {"experiment_nanopore_id", "analyte_id"},
    "aligned_nanopore": {"aligned_nanopore_id", "experiment_nanopore_id"},
}

REFERENCE_SOURCE = {
    # source table : primary_key
    "analyte": "analyte_id",
    "experiment_dna_short_read": "experiment_dna_short_read_id",
    "experiment_nanopore": "experiment_nanopore_id",
    "family": "family_id",
    "participant": "participant_id",
}


CROSS_REF_CHECK = [
    # table_name : # list of foreign keys
    ("aligned_dna_short_read", "experiment_dna_short_read_id"),
    ("aligned_nanopore", "experiment_nanopore_id"),
    ("analyte", "participant_id"),
    ("experiment_dna_short_read", "analyte_id"),
    ("experiment_nanopore", "analyte_id"),
    ("genetic_findings", "participant_id"),
    ("participant", "family_id"),
    ("phenotype", "participant_id"),
]
