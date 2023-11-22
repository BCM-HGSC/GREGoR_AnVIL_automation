"""Custom cerberus validator for GREGoR project"""
from datetime import datetime

from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def _check_with_is_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA`"""
        if value != "NA":
            self._error(field, "Value must be NA")

    def _check_with_is_number(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if not isinstance(value, int):
            self._error(field, "Value requires an int")

    def _check_with_is_number_or_is_na(self, field: str, value: str):
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
        # TODO: Please fill out.
        if value != 0 and (
            not value.startswith("BCM_Subject_") or not value.endswith("_2")
        ):  # add and not the subject id match, WIP
            self._error(
                field,
                "Value must be 0 or match the format of BCM_Subject_######_2, and match the subject id in participant_id",
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
        # TODO: Please fill out.
        if value != 0 and (
            not value.startswith("BCM_Subject_") or not value.endswith("_3")
        ):  # add and not the subject id match, WIP
            self._error(
                field,
                "Value must be 0 or match the format of BCM_Subject_######_3, and match the subject id in participant_id",
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
        # TODO: Please fill out.
        # NOTE: Twin ID field looks like this for reference: BCM_Subject_BH10325_1 BCM_Subject_BH10325_4
        error = [
            "Value must be NA or:",
            "Value must contain two strings separated by a space.",
            "One string must match the format of BCM_Subject_######_1.",
            "The other string must match the format of BCM_Subject_######_4.",
            "Both strings must have the same subject_id.",
            "One of the strings must be the same as participant_id.",
        ]
        if value != "NA":
            if value.count(" ") == 1:
                id1 = value.split(" ")[0]
                id2 = value.split(" ")[1]
                start_idx = len("BCM_Subject_")
                end_idx1 = len(id1) - len("_#")
                end_idx2 = len(id2) - len("_#")
                if (
                    not id1.startswith("BCM_Subject_")
                    or not id2.startswith("BCM_Subject_")
                    or not (
                        (id1.endswith("_4") and id2.endswith("_1"))
                        or (id1.endswith("_1") and id2.endswith("_4"))
                    )
                    or id1[start_idx:end_idx1] != id2[start_idx:end_idx2]
                ):
                    # Need to add check for being same as participant_id
                    self._error(field, "\n".join(error))

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

    def _normalize_coerce_camelcase(self, value: str) -> str:
        """Coerces value to camelcase"""
        value = value[0].upper() + value[1:].lower()
        return value

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to uppercase"""
        value = value.upper()
        return value

    def _normalize_coerce_year_month_date(self, value: str) -> str:
        """Coerces value to YYY-MM-DD format"""
        value = datetime.strptime(value, "%Y-%m-%d")
        return value
