from decimal import Decimal
from typing import Dict, Any
from .base_validator import BaseValidator, ValidationError


class CdValidator(BaseValidator):
    @staticmethod
    def validate_title(title: str) -> str:
        CdValidator.validate_required(title, "CD title")
        CdValidator.validate_min_length(title, 2, "CD title")

        return title.strip().title()

    @staticmethod
    def validate_rental_price(rental_price) -> Decimal:
        CdValidator.validate_required(rental_price, "Rental price")

        try:
            price = Decimal(str(rental_price))
            if price <= 0:
                raise ValueError("Rental price must be positive")
            return price
        except (ValueError, TypeError):
            raise ValueError("Rental price must be a valid number")

    @staticmethod
    def validate_cd_data(title: str, rental_price) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate title
        try:
            results["title"] = CdValidator.validate_title(title)
        except ValueError as e:
            errors.append(str(e))

        # Validate rental price
        try:
            results["rental_price"] = CdValidator.validate_rental_price(rental_price)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results 