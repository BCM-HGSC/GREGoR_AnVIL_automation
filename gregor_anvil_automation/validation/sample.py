"""Custom cerberus validator for GREGoR project"""
from datetime import datetime
from string import capwords

from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def __init__(self, batch_id, gcp_bucket, *args, **kwargs):
        super(Validator, self).__init__(*args, **kwargs)
        self.batch_id = batch_id
        self.gcp_bucket = gcp_bucket

    def _check_with_aligned_nanopore_id(self, field: str, value: str):
        """Check that `aligned_nanopore_id` is valid.
        Valid if:
            - {experiment_nanopore_id}_{batch_id}
        """
        # TODO: Please fill out

    def _check_with_experiment_nanopore_id(self, field: str, value: str):
        """Check that `experiment_nanopore_id` is valid.
        Valid if:
            - BCM_ONTWGS_*
        """

    def _check_with_analyte_id(self, field: str, value: str):
        """Checks that the analyte_id is valid:
        Valid if:
            - {participant_id}_{batch_id}"""
        # TODO: Please fill out

    def _check_with_experiment_dna_short_read_id(self, field: str, value: str):
        """Checks that the `experiment_dna_short_read_id` is valid.
        Valid if:
            - experiment_dna_short_read_id == aligned_dna_short_read_id WITHOUT
                the batch id.
        """

    def _check_with_experiment_sample_id(self, field: str, value: str):
        """Checks that the `experiment_sample_id`
        Valid if:
            - experiment_sample_id == experiment_dna_short_read_id
              (without the BCM part)
        """
        # TODO: Please fill out

    def _check_with_is_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA`"""
        if value != "NA":
            self._error(field, "Value must be NA")

    def _check_with_is_number(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if not isinstance(value, int):
            self._error(field, "Value requires an int")

    def _check_with_is_number_or_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA` or a valid integer"""
        if value != "NA" and not isinstance(value, int):
            self._error(field, "Value must be NA or an int")

    def _check_with_maternal_id_is_valid(self, field: str, value: str):
        """Checks that maternal id is valid.
        A valid maternal id is:
            - starts with BCM_Subject_
            - ends with _2
            - the subject id matches the subject id in `participant_id`
        Special Condition:
            - "0" must be accepted as valid input
        """
        participant_id = self.document["participant_id"]
        maternal_id = "_".join(participant_id.split("_")[:-1]) + "_2"
        if not self.document["participant_id"].endswith("_1"):
            if value != "0":
                self._error(
                    field,
                    'Value must be "0" or match the format of BCM_Subject_######_2, and match the subject id in `participant_id`',
                )
        elif value != maternal_id:
            self._error(
                field,
                'Value must be "0" or match the format of BCM_Subject_######_2, and match the subject id in `participant_id`',
            )

    def _check_with_paternal_id_is_valid(self, field: str, value: str):
        """Checks that paternal id is valid.
        A valid paternal id is:
            - starts with BCM_Subject_
            - ends with _3
            - the subject id matches the subject id in `participant_id`
        Special Condition:
            - "0" must be accepted as valid input
        """
        participant_id = self.document["participant_id"]
        paternal_id = "_".join(participant_id.split("_")[:-1]) + "_3"
        if not self.document["participant_id"].endswith("_1"):
            if value != "0":
                self._error(
                    field,
                    'Value must be "0" or match the format of BCM_Subject_######_3, and match the subject id in `participant_id`',
                )
        elif value != paternal_id:
            self._error(
                field,
                'Value must be "0" or match the format of BCM_Subject_######_3, and match the subject id in `participant_id`',
            )

    def _check_with_twin_id_is_valid(self, field: str, value: str):
        """Checks that twin id is valid.
        A valid twin id is:
            - the `participant_id` must be one of the twin ids
            - the other id must end with either a _1 or _4
            - both ids must start with BCM_Subject_
            - both ids must contain the same subject_id
        Special Condition:
            - "NA" must be accepted as valid input
        """
        participant_id = self.document["participant_id"]
        subject_id = participant_id.split("_")[2]
        matching = f"BCM_Subject_{subject_id}_"
        ids = value.split(" ")
        if value != "NA":
            if len(ids) != 2:
                self._error(field, "Value does not have exactly two ids")
            if not (
                (ids[0].endswith("_1") and ids[1].endswith("_4"))
                or (ids[0].endswith("_4") and ids[1].endswith("_1"))
            ):
                self._error(
                    field, "Ids do not end with _1 and _4 or _4 and _1 respectively."
                )
            for twin_id in ids[:2]:
                if participant_id == twin_id:
                    participant_id_exist = True
                    continue
                if matching not in twin_id:
                    self._error(field, f"{value} does not contain {matching}")
            if not participant_id_exist:
                self._error(field, "Value does not contain `participant_id`")

    def _check_with_must_start_with_bcm(self, field: str, value: str):
        """Checks that field's value starts with `BCM_`"""
        if not value.startswith("BCM_"):
            self._error(field, "Value must start with BCM_")

    def _check_with_must_start_with_bcm_fam(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Fam`"""
        if not value.startswith("BCM_Fam"):
            self._error(field, "Value must start with BCM_Fam")

    def _check_with_must_start_with_bcm_subject(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Subject`"""
        if not value.startswith("BCM_Subject"):
            self._error(field, "Value must start with BCM_Subject")

    def _check_with_must_start_with_bcm_subject_or_is_na(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Subject` or is na"""
        if value != "NA" and not value.startswith("BCM_Subject"):
            self._error(field, "Value must be NA or start with BCM_Subject")

    def _check_with_must_start_with_ontology(self, field: str, value: str):
        """Checks that field's value starts with `HP:` or `MONDO:`"""
        ontology = ["HP:", "MONDO:"]
        if not value.startswith(tuple(ontology)):
            self._error(field, "Value must start with HP: or MONDO:")

    def _normalize_coerce_initialcase(self, value: str) -> str:
        """Coerces value to initialcase"""
        if value.strip():
            value = capwords(value)
        return value

    def _normalize_coerce_titlecase(self, value: str) -> str:
        """Coerces value to titlecase"""
        if value.strip():
            value.title()
        return value

    def _normalize_coerce_lowercase(self, value: str) -> str:
        """Coerces value to lowercase"""
        return value.lower() if value else value

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to uppercase"""
        return value.upper() if value else value

    def _normalize_coerce_year_month_date(self, value: str) -> str:
        """Coerces value to YYY-MM-DD format"""
        value = datetime.strptime(value, "%Y-%m-%d")
        return value

    def _normalize_coerce_into_gcp_path_if_not_na(self, value: str) -> str:
        """Coerce value into a gcp path if not NA."""
        # TODO: Please fill out.
        # NOTE: If anything but NA given, format as `gs://{google_bucket}/{value}`

    def _normalize_coerce_aligned_dna_short_read_file(self, value: str):
        """Coerce `aligned_dna_short_read_file` to a GCP path."""
        # TODO: Please fill out :)
        # NOTE: Expected format. gs://{bucket_name}/{aligned_dna_short_read_id}.hgv.cram
        # Might get updated depending on https://github.com/BCM-HGSC/GREGoR_AnVIL_automation/issues/31

    def _normalize_coerce_aligned_dna_short_read_index_file(self, value: str):
        """Coerce `aligned_dna_short_read_index_file` to a GCP path."""
        # TODO: Please fill out :)
        # NOTE: Expected format. gs://{bucket_name}/{aligned_dna_short_read_id}.hgv.cram.crai
        # Might get updated depending on https://github.com/BCM-HGSC/GREGoR_AnVIL_automation/issues/31

    def _normalize_coerce_aligned_nanopore_file(self, value: str):
        """Coerce `aligned_nanopore_file` to a GCP path that ends with .bam"""
        # TODO: Please fill out
        # NOTE: Expected format. gs://{bucket_name}/{aligned_nanopore_id}.bam

    def _normalize_coerce_aligned_nanopore_index_file(self, value: str):
        """Coerce `aligned_nanopore_index_file` to a GCP path that ends with .bam.bai"""
        # TODO: Please fill out
        # NOTE: Expected format. gs://{bucket_name}/{aligned_nanopore_id}.bam.bai
