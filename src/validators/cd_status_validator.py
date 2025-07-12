from typing import Dict
from .base_validator import BaseValidator, ValidationError


class CdStatusValidator(BaseValidator):
    VALID_STATUSES = ["available", "rented", "maintenance", "damaged", "lost"]

    @staticmethod
    def validate_description(description: str) -> str:
        CdStatusValidator.validate_required(description, "CD status description")

        # Normalize the input
        description_lower = description.strip().lower()

        if description_lower not in CdStatusValidator.VALID_STATUSES:
            raise ValueError(
                f"CD status must be one of: {', '.join(CdStatusValidator.VALID_STATUSES)}"
            )

        return description_lower

    @staticmethod
    def validate_cd_status_data(description: str) -> Dict[str, str]:
        errors = []
        results = {}

        # Validate description
        try:
            results["description"] = CdStatusValidator.validate_description(description)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
