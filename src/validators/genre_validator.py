from typing import Dict
from .base_validator import BaseValidator, ValidationError


class GenreValidator(BaseValidator):
    @staticmethod
    def validate_description(description: str) -> str:
        GenreValidator.validate_required(description, "Genre description")
        GenreValidator.validate_min_length(description, 2, "Genre description")

        return description.strip().title()

    @staticmethod
    def validate_genre_data(description: str) -> Dict[str, str]:
        errors = []
        results = {}

        # Validate description
        try:
            results["description"] = GenreValidator.validate_description(description)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
