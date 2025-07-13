from uuid import UUID
from typing import Dict, Any
from .base_validator import BaseValidator, ValidationError


class AttendantValidator(BaseValidator):
    @staticmethod
    def validate_person_id(person_id) -> UUID:
        AttendantValidator.validate_required(person_id, "Person ID")

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
    def validate_store_id(store_id) -> UUID:
        AttendantValidator.validate_required(store_id, "Store ID")

        try:
            if isinstance(store_id, str):
                return UUID(store_id)
            elif isinstance(store_id, UUID):
                return store_id
            else:
                raise ValueError("Store ID must be a valid UUID")
        except (ValueError, TypeError):
            raise ValueError("Store ID must be a valid UUID")

    @staticmethod
    def validate_attendant_data(person_id, store_id) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate person_id
        try:
            results["person_id"] = AttendantValidator.validate_person_id(person_id)
        except ValueError as e:
            errors.append(str(e))

        # Validate store_id
        try:
            results["store_id"] = AttendantValidator.validate_store_id(store_id)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
