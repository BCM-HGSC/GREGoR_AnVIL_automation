"""Custom cerberus validator for GREGoR project"""
from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def _check_with_is_number(self, field: str, value: str):
        """Checks that the field's value is a valid integer"""
        if isinstance(value, int):
            self._error(field, "Value requires an int")

    def _check_with_must_start_with_bcm_fam(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Fam`"""
        if not value.startswith("BCM_Fam"):
            self._error(field, "Value must start with BCM_Fam")

    def _check_with_must_start_with_bcm_subject(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Subject`"""
        if not value.startswith("BCM_Subject"):
            self._error(field, "Value must start with BCM_Subject")

    def _normalize_coerce_camelcase(self, value: str) -> str:
        """Coerces value to camelcase"""
        value = value[0].upper() + value[1:].lower()
        return value

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to uppercase"""
        value = value.upper()
        return value
