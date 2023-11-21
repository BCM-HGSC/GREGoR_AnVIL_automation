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
