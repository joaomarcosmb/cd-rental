from decimal import Decimal
from typing import Dict, Any
from .base_validator import BaseValidator, ValidationError


class AlbumValidator(BaseValidator):
    @staticmethod
    def validate_title(title: str) -> str:
        AlbumValidator.validate_required(title, "Album title")
        AlbumValidator.validate_min_length(title, 2, "Album title")

        return title.strip().title()

    @staticmethod
    def validate_rental_price(rental_price) -> Decimal:
        AlbumValidator.validate_required(rental_price, "Rental price")

        try:
            price = Decimal(str(rental_price))
            if price <= 0:
                raise ValueError("Rental price must be positive")
            return price
        except (ValueError, TypeError):
            raise ValueError("Rental price must be a valid number")

    @staticmethod
    def validate_artist(artist: str) -> str:
        AlbumValidator.validate_required(artist, "Artist")
        AlbumValidator.validate_min_length(artist, 2, "Artist")
        return artist.strip().title()

    @staticmethod
    def validate_genre(genre: str) -> str:
        AlbumValidator.validate_required(genre, "Genre")
        AlbumValidator.validate_min_length(genre, 2, "Genre")
        return genre.strip().title()

    @staticmethod
    def validate_album_data(
        title: str, rental_price, artist: str, genre: str
    ) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate title
        try:
            results["title"] = AlbumValidator.validate_title(title)
        except ValueError as e:
            errors.append(str(e))

        # Validate rental price
        try:
            results["rental_price"] = AlbumValidator.validate_rental_price(rental_price)
        except ValueError as e:
            errors.append(str(e))

        # Validate artist
        try:
            results["artist"] = AlbumValidator.validate_artist(artist)
        except ValueError as e:
            errors.append(str(e))

        # Validate genre
        try:
            results["genre"] = AlbumValidator.validate_genre(genre)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
