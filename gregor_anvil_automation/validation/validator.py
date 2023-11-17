"""Custom cerberus validator for GREGoR project"""
from datetime import datetime

from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def _check_with_is_number(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if not isinstance(value, int):
            self._error(field, "Value requires an int")

    def _check_with_is_number_or_na(self, field: str, value: str):
        """Checks that the field's value is the string `NA` or a valid integer"""
        if value != "NA" and not isinstance(value, int):
            self._error(field, "Value must be NA or an int")

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
