from uuid import UUID
from typing import Dict, Any
from .base_validator import BaseValidator, ValidationError


class CustomerValidator(BaseValidator):
    @staticmethod
    def validate_person_id(person_id) -> UUID:
        CustomerValidator.validate_required(person_id, "Person ID")

        try:
            if isinstance(person_id, str):
                return UUID(person_id)
            elif isinstance(person_id, UUID):
                return person_id
            else:
                raise ValueError("Person ID must be a valid UUID")
        except (ValueError, TypeError):
            raise ValueError("Person ID must be a valid UUID")

    @staticmethod
    def validate_customer_data(person_id) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate person_id
        try:
            results["person_id"] = CustomerValidator.validate_person_id(person_id)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
