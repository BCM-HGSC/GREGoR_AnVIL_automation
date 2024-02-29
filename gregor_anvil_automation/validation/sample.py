"""Custom cerberus validator for GREGoR project"""

from datetime import datetime
from string import capwords

from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def __init__(self, batch_number, gcp_bucket, *args, **kwargs):
        super(Validator, self).__init__(*args, **kwargs)
        self.batch_number = batch_number
        self.gcp_bucket = gcp_bucket

    def _check_with_aligned_nanopore_id(self, field: str, value: str):
        """Checks that `aligned_nanopore_id` is valid.
        Valid if:
            - Starts with {experiment_nanopore_id}_A
            - Ends with a number between 1 and {batch_number}, inclusively
        """
        experiment_nanopore_id = self.document.get("experiment_nanopore_id")
        if not experiment_nanopore_id:
            return
        try:
            value_number = int(value.split(f"{experiment_nanopore_id}_A")[-1])
            if not value.startswith(f"{experiment_nanopore_id}_A") or not (
                1 <= value_number <= self.batch_number
            ):
                raise ValueError
        except ValueError:
            self._error(
                field,
                f"Value must start with {experiment_nanopore_id}_A and end with a number between 1 and {self.batch_number}, inclusively",
            )

    def _check_with_aligned_dna_short_read_id(self, field: str, value: str):
        """Checks that `aligned_dna_short_read_id` is valid.
        Valid if:
            - Starts with BCM_
            - Ends with a number between 1 and {batch_number}, inclusively
        """
        try:
            value_number = int(value.split("_A")[-1])
            if not value.startswith("BCM_") or not (
                1 <= value_number <= self.batch_number
            ):
                raise ValueError
        except ValueError:
            self._error(
                field,
                f"Value must start with BCM_ and end with _A{self.batch_number}, inclusively",
            )

    def _check_with_experiment_nanopore_id_start(self, field: str, value: str):
        """Checks that `experiment_nanopore_id` has a valid start.
        Valid if:
            - Starts with BCM_ONTWGS_BH
        """
        if not value.startswith("BCM_ONTWGS_BH"):
            self._error(
                field,
                "Value must start with BCM_ONTWGS_BH",
            )

    def _check_with_experiment_nanopore_id_end(self, field: str, value: str):
        """Checks that `experiment_nanopore_id` has a valid end.
        Valid if:
            - Ends with _{some_number}
        """
        end_string = ""
        if value.split("_")[-1]:
            end_string = value.split("_")[-1]
        if not end_string.isnumeric():
            self._error(
                field,
                "Value must end with _{some_number}",
            )

    def _check_with_analyte_id(self, field: str, value: str):
        """Checks that the analyte_id is valid:
        Valid if:
            - Starts with BCM_Subject_
            - Ends in _1_A, _2_A, _3_A, or _4_A and then a number between 1 and {batch_number}, inclusively
        """
        if value.startswith("BCM_Subject_"):
            if int(value.split("_A")[-1]):
                value_number = int(value.split("_A")[-1])
            else:
                return
        if (
            not value.startswith("BCM_Subject_")
            or not (1 <= value_number <= self.batch_number)
            or not value.endswith(
                (
                    f"_1_A{value_number}",
                    f"_2_A{value_number}",
                    f"_3_A{value_number}",
                    f"_4_A{value_number}",
                )
            )
        ):
            self._error(
                field,
                f"Value must start with BCM_Subject_ and ends with _1_A, _2_A, _3_A, or _4_A and then a number between 1 and {self.batch_number}, inclusively",
            )

    def _check_with_analyte_id_matches_participant_id(self, field: str, value: str):
        """Checks that the analyte_id is valid:
        Valid if:
            - Starts with {participant_id}_A
            - Ends with a number between 1 and {batch_number}, inclusively
        """
        participant_id = self.document.get("participant_id")
        if not participant_id:
            return
        try:
            value_number = int(value.split(f"{participant_id}_A")[-1])
            if not value.startswith(f"{participant_id}_A") or not (
                1 <= value_number <= self.batch_number
            ):
                raise ValueError
        except ValueError:
            self._error(
                field,
                f"Value must start with {participant_id}_A and end with a number between 1 and {self.batch_number}, inclusively",
            )

    def _check_with_experiment_dna_short_read_id(self, field: str, value: str):
        """Checks that the `experiment_dna_short_read_id` is valid.
        Valid if:
            - experiment_dna_short_read_id == aligned_dna_short_read_id WITHOUT
                the batch_number.
        """
        aligned_dna_short_read_id = self.document.get("aligned_dna_short_read_id")
        if not aligned_dna_short_read_id:
            return
        experiment_dna_short_read_id = aligned_dna_short_read_id.split("_A")[0]
        if value != experiment_dna_short_read_id:
            self._error(
                field,
                f"Value must match the format of {aligned_dna_short_read_id} minus _A{self.batch_number}",
            )

    def _check_with_experiment_sample_id(self, field: str, value: str):
        """Checks that the `experiment_sample_id` is valid.
        Valid if:
            - experiment_sample_id == experiment_dna_short_read_id
              (without the BCM part)
        """
        experiment_dna_short_read_id = self.document.get("experiment_dna_short_read_id")
        if not experiment_dna_short_read_id:
            return
        experiment_sample_id = experiment_dna_short_read_id.replace("BCM_", "")
        if value != experiment_sample_id:
            self._error(
                field,
                f"Value must match the format of {experiment_dna_short_read_id} minus BCM_",
            )

    def _check_with_is_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA`"""
        if value.strip().upper() != "NA":
            self._error(field, "Value must be NA")

    def _check_with_is_number(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if not value.isdigit():
            self._error(field, "Value requires an int")

    def _check_with_is_number_or_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA` or a valid integer"""
        if value.strip().upper() != "NA" and not value.isdigit():
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
        participant_id = self.document.get("participant_id")
        if not participant_id or value == "0":
            return
        maternal_id = "_".join(participant_id.split("_")[:-1]) + "_2"
        if not self.document["participant_id"].endswith("_1") or value != maternal_id:
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
        participant_id = self.document.get("participant_id")
        if not participant_id or value == "0":
            return
        paternal_id = "_".join(participant_id.split("_")[:-1]) + "_3"
        if not self.document["participant_id"].endswith("_1") or value != paternal_id:
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
        participant_id = self.document.get("participant_id")
        if not participant_id or value == "NA":
            return
        if participant_id not in value:
            self._error(field, "Value does not contain `participant_id`")
            return
        if len(value.split(" ")) != 2:
            self._error(field, "Value does not have exactly two ids")
            return
        subject_id = participant_id.split("_")[2]
        matching = (
            f"BCM_Subject_{subject_id}_{'4' if participant_id.endswith('_1') else '1'}"
        )
        twin_id = value.replace(participant_id, "").strip()
        if twin_id != matching:
            self._error(field, f"Twin id does not match expected format of: {matching}")

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
        if value.strip().upper() != "NA" and not value.startswith("BCM_Subject"):
            self._error(field, "Value must be NA or start with BCM_Subject")

    def _check_with_must_start_with_ontology(self, field: str, value: str):
        """Checks that field's value starts with `HP:` or `MONDO:`"""
        ontology = ["HP:", "MONDO:"]
        if not value.startswith(tuple(ontology)):
            self._error(field, "Value must start with HP: or MONDO:")

    def _normalize_coerce_initialcase(self, value: str) -> str:
        """Coerces value to initialcase"""
        if value.strip():
            value = value.capitalize()
        return value

    def _normalize_coerce_titlecase(self, value: str) -> str:
        """Coerces value to titlecase"""
        if value.strip():
            value = capwords(value)
        return value

    def _normalize_coerce_lowercase(self, value: str) -> str:
        """Coerces value to lowercase"""
        return value.lower() if value else value

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to uppercase"""
        return value.upper() if value else value

    def _normalize_coerce_year_month_date(self, value: str) -> str:
        """Coerces values with the format of:
        - M/D/YY
        - M-D-YY
        - M/D/YYYY
        - M-D-YYYY
        - MM/DD/YYYY
        - MM-DD-YYYY
        - YYYY/MM/DD
        to the format of YYYY-MM-DD
        """
        if value == "NA":
            return value
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m-%d-%Y",
            "%m/%d/%Y",
        ]
        for date_string in formats:
            try:
                value = datetime.strftime(
                    datetime.strptime(value, date_string), "%Y-%m-%d"
                )
            except ValueError:
                pass
        # try:
        #     month_substring = value.split("-")[0]
        #     month = f"0{month_substring}"
        #     date_substring = value.split("-")[1]
        #     date = f"0{date_substring}"
        #     year = int(value.split("-")[2])
        #     if year < 100:
        #         if year > 96:
        #             year = f"19{year}"
        #         else:
        #             year = f"20{year}"
        #             # Will need update come year 2100
        #     elif year < 1000:
        #         return value
        #     value = f"{year}-{month}-{date}"
        # except ValueError:
        #     pass
        # try:
        #     month_substring = value.split("/")[0]
        #     month = f"0{month_substring}"
        #     date_substring = value.split("/")[1]
        #     date = f"0{date_substring}"
        #     year = int(value.split("/")[2])
        #     if year < 100:
        #         if year > 96:
        #             year = f"19{year}"
        #         else:
        #             year = f"20{year}"
        #             # Will need update come year 2100
        #     elif year < 1000:
        #         return value
        #     value = f"{year}-{month}-{date}"
        # except ValueError:
        #     pass
        return value

    def _normalize_coerce_into_gcp_path_if_not_na(self, value: str) -> str:
        """Coerce value into a gcp path if not NA.
        Expected format: "NA" or `gs://{google_bucket}/{value}`
        """
        if value.strip().upper() != "NA":
            value = f"gs://{self.gcp_bucket}/{value}"
        return value

    def _normalize_coerce_aligned_dna_short_read_file(self, value: str):
        """Coerce `aligned_dna_short_read_file` to a GCP path.
        Expected format: gs://{bucket_name}/{aligned_dna_short_read_id}.hgv.cram
        Might get updated depending on https://github.com/BCM-HGSC/GREGoR_AnVIL_automation/issues/31
        """
        aligned_dna_short_read_id = self.document.get("aligned_dna_short_read_id")
        if not aligned_dna_short_read_id:
            return value
        if not value:
            value = f"gs://{self.gcp_bucket}/{aligned_dna_short_read_id}.hgv.cram"
        return value

    def _normalize_coerce_aligned_dna_short_read_index_file(self, value: str):
        """Coerce `aligned_dna_short_read_index_file` to a GCP path.
        Expected format: gs://{bucket_name}/{aligned_dna_short_read_id}.hgv.cram.crai
        Might get updated depending on https://github.com/BCM-HGSC/GREGoR_AnVIL_automation/issues/31
        """
        aligned_dna_short_read_id = self.document.get("aligned_dna_short_read_id")
        if not aligned_dna_short_read_id:
            return value
        if not value:
            value = f"gs://{self.gcp_bucket}/{aligned_dna_short_read_id}.hgv.cram.crai"
        return value

    def _normalize_coerce_aligned_nanopore_file(self, value: str):
        """Coerce `aligned_nanopore_file` to a GCP path that ends with .bam
        Expected format: gs://{bucket_name}/{aligned_nanopore_id}.bam
        """
        aligned_nanopore_id = self.document.get("aligned_nanopore_id")
        if not aligned_nanopore_id:
            return value
        if not value:
            value = f"gs://{self.gcp_bucket}/{aligned_nanopore_id}.bam"
        return value

    def _normalize_coerce_aligned_nanopore_index_file(self, value: str):
        """Coerce `aligned_nanopore_index_file` to a GCP path that ends with .bam.bai
        Expected format. gs://{bucket_name}/{aligned_nanopore_id}.bam.bai
        """
        aligned_nanopore_id = self.document.get("aligned_nanopore_id")
        if not aligned_nanopore_id:
            return value
        if not value:
            value = f"gs://{self.gcp_bucket}/{aligned_nanopore_id}.bam.bai"
        return value
