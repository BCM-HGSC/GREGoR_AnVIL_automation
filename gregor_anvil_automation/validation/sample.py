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
        if self.document["experiment_nanopore_id"]:
            experiment_nanopore_id = self.document["experiment_nanopore_id"]
        aligned_nanopore_id = f"{experiment_nanopore_id}_{self.batch_id}"
        if value != aligned_nanopore_id:
            self._error(
                field,
                f"Value must match the format of {experiment_nanopore_id}_{self.batch_id}",
            )

    def _check_with_aligned_dna_short_read_id(self, field: str, value: str):
        """Check that `aligned_dna_short_read_id` is valid.
        Valid if:
            - Starts with BCM_
            - Ends in _{batch_id}
        """
        if not value.startswith("BCM_") or not value.endswith((f"_{self.batch_id}")):
            self._error(
                field, f"Value must start with BCM_ and end with _{self.batch_id}"
            )

    def _check_with_experiment_nanopore_id(self, field: str, value: str):
        """Check that `experiment_nanopore_id` is valid.
        Valid if:
            - BCM_ONTWGS_*
        """
        if not value.startswith("BCM_ONTWGS_"):
            self._error(
                field,
                "Value must start with BCM_ONTWGS_",
            )

    def _check_with_analyte_id(self, field: str, value: str):
        """Checks that the analyte_id is valid:
        Valid if:
            - Starts with BCM_Subject_
            - Ends in _1_{batch_id}, _2_{batch_id}, _3_{batch_id}, or _4_{batch_id}"""
        if not value.startswith("BCM_Subject_") or not value.endswith(
            (
                f"_1_{self.batch_id}",
                f"_2_{self.batch_id}",
                f"_3_{self.batch_id}",
                f"_4_{self.batch_id}",
            )
        ):
            self._error(
                field,
                f"Value must start with BCM_Subject_ and end with _1_{self.batch_id}, _2_{self.batch_id}, _3_{self.batch_id}, or _4_{self.batch_id}",
            )

    def _check_with_analyte_id_matches_participant_id(self, field: str, value: str):
        """Checks that the analyte_id is valid:
        Valid if:
            - {participant_id}_{batch_id}"""
        if self.document["participant_id"]:
            participant_id = self.document["participant_id"]
        analyte_id = f"{participant_id}_{self.batch_id}"
        if value != analyte_id:
            self._error(field, f"Value must match the format of {analyte_id}")

    def _check_with_experiment_dna_short_read_id(self, field: str, value: str):
        """Checks that the `experiment_dna_short_read_id` is valid.
        Valid if:
            - experiment_dna_short_read_id == aligned_dna_short_read_id WITHOUT
                the batch id.
        """
        if self.document["aligned_dna_short_read_id"]:
            aligned_dna_short_read_id = self.document["aligned_dna_short_read_id"]
        experiment_dna_short_read_id = aligned_dna_short_read_id.replace(
            f"_{self.batch_id}", ""
        )
        if value != experiment_dna_short_read_id:
            self._error(
                field,
                f"Value must match the format of {aligned_dna_short_read_id} minus _{self.batch_id}",
            )

    def _check_with_experiment_sample_id(self, field: str, value: str):
        """Checks that the `experiment_sample_id` is valid.
        Valid if:
            - experiment_sample_id == experiment_dna_short_read_id
              (without the BCM part)
        """
        if self.document["experiment_dna_short_read_id"]:
            experiment_dna_short_read_id = self.document["experiment_dna_short_read_id"]
        experiment_sample_id = experiment_dna_short_read_id.replace("BCM_", "")
        if value != experiment_sample_id:
            self._error(
                field,
                f"Value must match the format of {experiment_dna_short_read_id} minus BCM_",
            )

    def _check_with_is_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA`"""
        if value != "NA":
            self._error(field, "Value must be NA")

    def _check_with_is_number(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if not value.isdigit():
            self._error(field, "Value requires an int")

    def _check_with_is_number_or_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA` or a valid integer"""
        if value != "NA" and not value.isdigit():
            self._error(field, "Value must be NA or an int")

    def _check_with_participant_id(self, field: str, value: str):
        """Checks that participant id is valid.
        A valid participant id is:
            - starts with BCM_Subject_
            - ends with _1, _2, _3, or _4
        """
        if not value.startswith("BCM_Subject_") or not value.endswith(
            ("_1", "_2", "_3", "_4")
        ):
            self._error(
                field,
                "Value must start with BCM_Subject and end with either _1, _2, _3, or _4",
            )

    def _check_with_maternal_id_is_valid(self, field: str, value: str):
        """Checks that maternal id is valid.
        A valid maternal id is:
            - starts with BCM_Subject_
            - ends with _2
            - the subject id matches the subject id in `participant_id`
        Special Condition:
            - "0" must be accepted as valid input
        """
        if self.document["participant_id"]:
            participant_id = self.document["participant_id"]
        maternal_id = "_".join(participant_id.split("_")[:-1]) + "_2"
        if value != "0":
            if (
                not self.document["participant_id"].endswith("_1")
                or value != maternal_id
            ):
                self._error(
                    field,
                    "Value must be '0' or match the format of BCM_Subject_######_2, and match the subject id in `participant_id`",
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
        if self.document["participant_id"]:
            participant_id = self.document["participant_id"]
        paternal_id = "_".join(participant_id.split("_")[:-1]) + "_3"
        if value != "0":
            if (
                not self.document["participant_id"].endswith("_1")
                or value != paternal_id
            ):
                self._error(
                    field,
                    "Value must be '0' or match the format of BCM_Subject_######_3, and match the subject id in `participant_id`",
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
        if (
            self.document["participant_id"]
            and len(self.document["participant_id"].split("_")) >= 3
        ):
            participant_id = self.document["participant_id"]
            subject_id = participant_id.split("_")[2]
            matching = f"BCM_Subject_{subject_id}_"
            participant_id_exist = False
            ids = value.split(" ")
            if value != "NA":
                if len(ids) != 2:
                    self._error(field, "Value does not have exactly two ids")
                else:
                    for twin_id in ids[:2]:
                        if participant_id == twin_id:
                            participant_id_exist = True
                            continue
                        if matching not in twin_id and twin_id == ids[1]:
                            self._error(field, f"{value} does not contain {matching}")
                    if not participant_id_exist:
                        self._error(field, "Value does not contain `participant_id`")
                if not (
                    (ids[0].endswith("_1") and ids[1].endswith("_4"))
                    or (ids[0].endswith("_4") and ids[1].endswith("_1"))
                ):
                    self._error(
                        field,
                        "Ids do not end with _1 and _4 or _4 and _1 respectively.",
                    )
        else:
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
            value = value.capitalize()
        return value

    def _normalize_coerce_lowercase(self, value: str) -> str:
        """Coerces value to lowercase"""
        return value.lower() if value else value

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to uppercase"""
        return value.upper() if value else value

    def _normalize_coerce_year_month_date(self, value: str) -> str:
        """Coerces value of MM-DD-YYYY, MM/DD/YYYY, or YYYY-MM-DD to YYYY-MM-DD format"""
        try:
            value = datetime.strftime(datetime.strptime(value, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            try:
                value = datetime.strftime(
                    datetime.strptime(value, "%m-%d-%Y"), "%Y-%m-%d"
                )
            except ValueError:
                value = datetime.strftime(
                    datetime.strptime(value, "%m/%d/%Y"), "%Y-%m-%d"
                )
        return value

    def _normalize_coerce_into_gcp_path_if_not_na(self, value: str) -> str:
        """Coerce value into a gcp path if not NA.
        Expected format: "NA" or `gs://{google_bucket}/{value}`
        """
        if value != "NA":
            value = f"gs://{self.gcp_bucket}/{value}"
        return value

    def _normalize_coerce_aligned_dna_short_read_file(self, value: str):
        """Coerce `aligned_dna_short_read_file` to a GCP path.
        Expected format: gs://{bucket_name}/{aligned_dna_short_read_id}.hgv.cram
        Might get updated depending on https://github.com/BCM-HGSC/GREGoR_AnVIL_automation/issues/31
        """
        if self.document["aligned_dna_short_read_id"]:
            aligned_dna_short_read_id = self.document["aligned_dna_short_read_id"]
        if value == "":
            value = f"gs://{self.gcp_bucket}/{aligned_dna_short_read_id}.hgv.cram"
        return value

    def _normalize_coerce_aligned_dna_short_read_index_file(self, value: str):
        """Coerce `aligned_dna_short_read_index_file` to a GCP path.
        Expected format: gs://{bucket_name}/{aligned_dna_short_read_id}.hgv.cram.crai
        Might get updated depending on https://github.com/BCM-HGSC/GREGoR_AnVIL_automation/issues/31
        """
        if self.document["aligned_dna_short_read_id"]:
            aligned_dna_short_read_id = self.document["aligned_dna_short_read_id"]
        if value == "":
            value = f"gs://{self.gcp_bucket}/{aligned_dna_short_read_id}.hgv.cram.crai"
        return value

    def _normalize_coerce_aligned_nanopore_file(self, value: str):
        """Coerce `aligned_nanopore_file` to a GCP path that ends with .bam
        Expected format: gs://{bucket_name}/{aligned_nanopore_id}.bam
        """
        if self.document["aligned_nanopore_id"]:
            aligned_nanopore_id = self.document["aligned_nanopore_id"]
        if value == "":
            value = f"gs://{self.gcp_bucket}/{aligned_nanopore_id}.bam"
        return value

    def _normalize_coerce_aligned_nanopore_index_file(self, value: str):
        """Coerce `aligned_nanopore_index_file` to a GCP path that ends with .bam.bai
        Expected format. gs://{bucket_name}/{aligned_nanopore_id}.bam.bai
        """
        if self.document["aligned_nanopore_id"]:
            aligned_nanopore_id = self.document["aligned_nanopore_id"]
        if value == "":
            value = f"gs://{self.gcp_bucket}/{aligned_nanopore_id}.bam.bai"
        return value
