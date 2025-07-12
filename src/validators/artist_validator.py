from typing import Dict
from .base_validator import BaseValidator, ValidationError


class ArtistValidator(BaseValidator):
    @staticmethod
    def validate_name(name: str) -> str:
        ArtistValidator.validate_required(name, "Artist name")
        ArtistValidator.validate_min_length(name, 2, "Artist name")

        return name.strip().title()

    @staticmethod
    def validate_artist_data(name: str) -> Dict[str, str]:
        errors = []
        results = {}

        # Validate name
        try:
            results["name"] = ArtistValidator.validate_name(name)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
