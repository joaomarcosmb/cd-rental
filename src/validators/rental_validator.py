from uuid import UUID
from datetime import datetime
from typing import Dict, Any, Optional
from .base_validator import BaseValidator, ValidationError


class RentalValidator(BaseValidator):
    @staticmethod
    def validate_customer_id(customer_id) -> UUID:
        RentalValidator.validate_required(customer_id, "Customer ID")

        try:
            if isinstance(customer_id, str):
                return UUID(customer_id)
            elif isinstance(customer_id, UUID):
                return customer_id
            else:
                raise ValueError("Customer ID must be a valid UUID")
        except (ValueError, TypeError):
            raise ValueError("Customer ID must be a valid UUID")

    @staticmethod
    def validate_item_id(item_id) -> UUID:
        RentalValidator.validate_required(item_id, "Item ID")

        try:
            if isinstance(item_id, str):
                return UUID(item_id)
            elif isinstance(item_id, UUID):
                return item_id
            else:
                raise ValueError("Item ID must be a valid UUID")
        except (ValueError, TypeError):
            raise ValueError("Item ID must be a valid UUID")

    @staticmethod
    def validate_attendant_id(attendant_id) -> UUID:
        RentalValidator.validate_required(attendant_id, "Attendant ID")

        try:
            if isinstance(attendant_id, str):
                return UUID(attendant_id)
            elif isinstance(attendant_id, UUID):
                return attendant_id
            else:
                raise ValueError("Attendant ID must be a valid UUID")
        except (ValueError, TypeError):
            raise ValueError("Attendant ID must be a valid UUID")

    @staticmethod
    def validate_rental_date(rental_date) -> datetime:
        if rental_date is None:
            return datetime.now()

        if isinstance(rental_date, datetime):
            return rental_date
        elif isinstance(rental_date, str):
            try:
                return datetime.fromisoformat(rental_date.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(
                    "Invalid rental date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        else:
            raise ValueError("Rental date must be a datetime object or ISO string")

    @staticmethod
    def validate_return_date(return_date, rental_date: datetime) -> Optional[datetime]:
        if return_date is None:
            return None

        if isinstance(return_date, datetime):
            validated_return_date = return_date
        elif isinstance(return_date, str):
            try:
                validated_return_date = datetime.fromisoformat(
                    return_date.replace("Z", "+00:00")
                )
            except ValueError:
                raise ValueError(
                    "Invalid return date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        else:
            raise ValueError("Return date must be a datetime object or ISO string")

        if validated_return_date <= rental_date:
            raise ValueError("Return date must be after rental date")

        return validated_return_date

    @staticmethod
    def validate_rental_data(
        customer_id, item_id, attendant_id, rental_date=None, return_date=None
    ) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate customer_id
        try:
            results["customer_id"] = RentalValidator.validate_customer_id(customer_id)
        except ValueError as e:
            errors.append(str(e))

        # Validate item_id
        try:
            results["item_id"] = RentalValidator.validate_item_id(item_id)
        except ValueError as e:
            errors.append(str(e))

        # Validate attendant_id
        try:
            results["attendant_id"] = RentalValidator.validate_attendant_id(
                attendant_id
            )
        except ValueError as e:
            errors.append(str(e))

        # Validate rental_date
        try:
            results["rental_date"] = RentalValidator.validate_rental_date(rental_date)
        except ValueError as e:
            errors.append(str(e))

        # Validate return_date (only if rental_date is valid)
        if "rental_date" in results:
            try:
                results["return_date"] = RentalValidator.validate_return_date(
                    return_date, results["rental_date"]
                )
            except ValueError as e:
                errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
