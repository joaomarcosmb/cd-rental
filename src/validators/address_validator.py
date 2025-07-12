import re
from typing import Dict
from .base_validator import BaseValidator, ValidationError


class AddressValidator(BaseValidator):
    @staticmethod
    def validate_street(street: str) -> str:
        AddressValidator.validate_required(street, "Street")
        AddressValidator.validate_min_length(street, 2, "Street")

        return street.strip().title()

    @staticmethod
    def validate_number(number: str) -> str:
        AddressValidator.validate_required(number, "Number")

        return str(number).strip()

    @staticmethod
    def validate_neighborhood(neighborhood: str) -> str:
        AddressValidator.validate_required(neighborhood, "Neighborhood")
        AddressValidator.validate_min_length(neighborhood, 2, "Neighborhood")

        return neighborhood.strip().title()

    @staticmethod
    def validate_city(city: str) -> str:
        AddressValidator.validate_required(city, "City")
        AddressValidator.validate_min_length(city, 2, "City")

        return city.strip().title()

    @staticmethod
    def validate_state(state: str) -> str:
        AddressValidator.validate_required(state, "State")
        AddressValidator.validate_exact_length(state.strip(), 2, "State")

        return state.strip().upper()

    @staticmethod
    def validate_zip_code(zip_code: str) -> str:
        AddressValidator.validate_required(zip_code, "ZIP code")

        zip_clean = re.sub(r"[^0-9]", "", zip_code)

        AddressValidator.validate_exact_length(zip_clean, 8, "ZIP code")

        return zip_clean

    @staticmethod
    def validate_address_data(
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        state: str,
        zip_code: str,
    ) -> Dict[str, str]:
        errors = []
        results = {}

        # Validate street
        try:
            results["street"] = AddressValidator.validate_street(street)
        except ValueError as e:
            errors.append(str(e))

        # Validate number
        try:
            results["number"] = AddressValidator.validate_number(number)
        except ValueError as e:
            errors.append(str(e))

        # Validate neighborhood
        try:
            results["neighborhood"] = AddressValidator.validate_neighborhood(
                neighborhood
            )
        except ValueError as e:
            errors.append(str(e))

        # Validate city
        try:
            results["city"] = AddressValidator.validate_city(city)
        except ValueError as e:
            errors.append(str(e))

        # Validate state
        try:
            results["state"] = AddressValidator.validate_state(state)
        except ValueError as e:
            errors.append(str(e))

        # Validate ZIP code
        try:
            results["zip_code"] = AddressValidator.validate_zip_code(zip_code)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
