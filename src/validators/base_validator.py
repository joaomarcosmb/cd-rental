from typing import List, Any, Callable


class ValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


class BaseValidator:
    @staticmethod
    def validate_required(value: Any, field_name: str) -> None:
        if not value:
            raise ValueError(f"{field_name} is required")

    @staticmethod
    def validate_min_length(value: str, min_length: int, field_name: str) -> None:
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")

    @staticmethod
    def validate_exact_length(value: str, length: int, field_name: str) -> None:
        if len(value) != length:
            raise ValueError(f"{field_name} must be exactly {length} characters")

    @staticmethod
    def validate_regex(
        value: str, pattern: str, field_name: str, error_message: str
    ) -> None:
        import re

        if not re.match(pattern, value):
            raise ValueError(f"{field_name} {error_message}")

    @staticmethod
    def collect_validation_errors(validation_functions: List[Callable]) -> None:
        errors = []

        for validation_func in validation_functions:
            try:
                validation_func()
            except ValueError as e:
                errors.append(str(e))

        if errors:
            raise ValidationError(errors)
