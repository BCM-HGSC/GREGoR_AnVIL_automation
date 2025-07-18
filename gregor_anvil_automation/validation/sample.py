"""Custom cerberus validator for GREGoR project"""

from datetime import datetime
from string import capwords

from cerberus import Validator
from dateutil.parser import parse

from gregor_anvil_automation.utils.mappings import (
    MULTI_FIELD_MAP,
    CAN_NOT_BE_NA,
    CONDITIONALLY_REQ_MAPPING,
)


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def __init__(self, batch_number, *args, **kwargs):
        super(Validator, self).__init__(*args, **kwargs)
        self.batch_number = batch_number

    def _check_with_is_gcp_path(self, field: str, value: str):
        """Checks that the given field is a google path path"""
        if value.lower() == "na" and field not in CAN_NOT_BE_NA:
            return
        if "gs://" not in value:
            self._error(field, "Does not contain a google path.")

    def _check_with_field_with_multi(self, field: str, value: str):
        """Checks that `additional_modifiers` has a valid one from
        the given dict.
        """
        if value == "NA":
            return
        parts = value.split("|")
        if not_valid := {
            part.strip() for part in parts if part.strip() not in MULTI_FIELD_MAP[field]
        }:
            self._error(
                field,
                f"Values ({not_valid}) are not accepted",
            )

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
            - Ends in _#_A{1<=} and then a number between 1 and {batch_number}, inclusively

        This should be used whenever `analyte_id` is not povided along with the `participant_id`.
        """
        error_message = f"Value must start with BCM_Subject_ and ends with _`a number`_A and then a number between 1 and {self.batch_number}, inclusively"
        if not value.startswith("BCM_Subject_"):
            self._error(
                field,
                error_message,
            )
            return

        parts = value.split("_")
        if len(parts) != 5:
            self._error(
                field,
                error_message,
            )
            return
        if not parts[3].isnumeric():
            self._error(
                field,
                error_message,
            )
            return
        try:
            given_batch_number = int(parts[-1][1:])
            int(parts[-2])
        except ValueError:
            self._error(
                field,
                error_message,
            )
            return
        if not 1 <= given_batch_number <= self.batch_number:
            self._error(
                field,
                error_message,
            )
            return

    def _check_with_analyte_id_matches_participant_id(self, field: str, value: str):
        """Checks that the analyte_id is valid:
        Valid if:
            - Starts with {participant_id}
            - Ends with a number between 1 and {batch_number}, inclusively
        """
        participant_id = self.document.get("participant_id").strip()
        analyte_type = self.document.get("analyte_type").strip()
        if not participant_id or not analyte_type:
            return
        if participant_id not in value:
            self._error(field, "Value must contain the participant_id.")
        batch_id = value.split(f"{participant_id}_")[-1]
        batch_type, batch_number = batch_id[0], int(batch_id[1:])
        if (analyte_type == "RNA" and batch_type != "R") or (
            analyte_type == "DNA" and batch_type != "A"
        ):
            self._error(
                field,
                "Value is using incorrect batch type identifier. Ex: Using `R` for DNA",
            )
        if not 1 <= batch_number <= self.batch_number:
            self._error(field, "Batch number should be >=1 and <= {self.batch_number}")

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
            - experiment_sample_id is not empty
        """
        if not value:
            self._error(
                field,
                "Value must not be empty",
            )

    def _check_with_is_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA`"""
        if value.strip().upper() != "NA":
            self._error(field, "Value must be NA")

    def _check_with_is_int(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if not value.isdigit():
            self._error(field, "Value requires an int")

    def _check_with_is_int_or_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA` or a valid integer"""
        if value.strip().upper() != "NA" and not value.isdigit():
            self._error(field, "Value must be NA or an int")

    def _check_with_is_float_or_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA` or a valid float"""
        if value.strip().upper() != "NA":
            try:
                float(value)
            except ValueError:
                self._error(field, "Value must be NA or a float")

    def _check_with_participant_id(self, field: str, value: str):
        """Checks that participant id is valid.
        A valid participant id is:
            - starts with BCM_Subject_
            - ends with _{a number}
        """
        end_string = value.split("_")[-1]
        if (
            not value.startswith("BCM_Subject_")
            or not end_string.isnumeric()
            or not value.endswith((f"_{end_string}"))
        ):
            self._error(
                field,
                "Value must start with BCM_Subject and end with _{a number}",
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
        participant_substring = "_".join(participant_id.split("_")[:-1])
        if not value.endswith("_2"):
            self._error(
                field,
                "Value does not end with _2",
            )
        if participant_substring not in value:
            self._error(
                field, "Field does not contain the same subject as the participant_id"
            )

    def _check_with_conditional_required(self, field: str, value: str):
        """Checks that a conditionally required field exist if that condition
        is met.
        """

        req_field, *allowed_values = CONDITIONALLY_REQ_MAPPING[field]
        req_field_value = self.document.get(req_field)
        if req_field_value in allowed_values and not value:
            # Not required
            self._error(
                field,
                f"Value is required since {req_field} is {req_field_value} and cannot be blank",
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
        participant_substring = "_".join(participant_id.split("_")[:-1])
        if not value.endswith("_3"):
            self._error(field, "Value does not end with _3")
        if participant_substring not in value:
            self._error(
                field, "Field does not contain the same subject as the participant_id"
            )

    def _check_with_twin_id_is_valid(self, field: str, value: str):
        """Checks that twin id is valid.
        A valid twin id is:
            - the `participant_id` cannot be one of the ids
        Special Condition:
            - "NA" must be accepted as valid input
        NOTE: We check that the ids are valid later on.
        """
        participant_id = self.document.get("participant_id")
        if not participant_id or value == "NA":
            return
        if participant_id in value:
            self._error(field, "Value should not contain `participant_id`")
            return

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

    def _check_with_gene_known_for_phenotype_is_known(self, field: str, value: str):
        """Checks that field's value is:
        - NA if gene_known_for_phenotype is Candidate or some string
        - A string other than NA if gene_known_for_phenotype is Known
        """
        gene_known_for_phenotype = self.document.get("gene_known_for_phenotype")
        if gene_known_for_phenotype == "Known" and (
            value == "" or value.lower() == "na"
        ):
            self._error(
                field, "Value may only be NA if gene_known_for_phenotype is not Known"
            )

    def _check_with_gene_known_for_phenotype_is_known_not_na(
        self, field: str, value: str
    ):
        """Checks that field's value is not empty if gene_known_for_phenotype is Known"""
        gene_known_for_phenotype = self.document.get("gene_known_for_phenotype")
        if gene_known_for_phenotype == "Known" and value == "":
            self._error(field, "Value is required if gene_known_for_phenotype is Known")

    def _normalize_coerce_multi(self, value: str) -> str:
        """Strips empty white spaces that can happen in muli-delimiter value"""
        return "|".join([v.strip() for v in value.split("|")])

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
        try:
            value = datetime.strftime(parse(value), "%Y-%m-%d")
        except ValueError:
            pass
        return value
