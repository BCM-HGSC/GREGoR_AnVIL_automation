"""Custom cerberus validator for GREGoR project"""
from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def _check_with_is_number(self, field: str, value: str):
        """Checks taht the field's value is a valid intenger"""
        # TODO: Add code

    def _check_with_must_start_with_bcm_fam(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Fam`"""
        # TODO: Add code

    def _check_with_must_start_with_bcm_subject(self, field: str, value: str):
        """Checks that field's value starts with `BCM_Subject`"""
        # TODO: Add code

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to camelcase"""
        # TODO: Add code
        return value

    def _normalize_coerce_uppercase(self, value: str) -> str:
        """Coerces value to uppercase"""
        # TODO: Add code
        return value
