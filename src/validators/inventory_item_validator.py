from uuid import UUID
from typing import Dict, Any
from .base_validator import BaseValidator, ValidationError


class InventoryItemValidator(BaseValidator):
    VALID_STATUSES = ["available", "rented", "maintenance", "damaged", "lost"]

    @staticmethod
    def validate_barcode(barcode: str) -> str:
        InventoryItemValidator.validate_required(barcode, "Barcode")
        InventoryItemValidator.validate_min_length(barcode, 2, "Barcode")

        # Remove any whitespace and convert to uppercase for consistency
        cleaned_barcode = barcode.strip().upper()

        # Validate that barcode contains only alphanumeric characters and hyphens
        import re

        if not re.match(r"^[A-Z0-9\-]+$", cleaned_barcode):
            raise ValueError(
                "Barcode must contain only alphanumeric characters and hyphens"
            )

        return cleaned_barcode

    @staticmethod
    def validate_album_id(album_id) -> UUID:
        InventoryItemValidator.validate_required(album_id, "Album ID")

        try:
            if isinstance(album_id, str):
                return UUID(album_id)
            elif isinstance(album_id, UUID):
                return album_id
            else:
                raise ValueError("Album ID must be a valid UUID")
        except (ValueError, TypeError):
            raise ValueError("Album ID must be a valid UUID")

    @staticmethod
    def validate_store_id(store_id) -> UUID:
        InventoryItemValidator.validate_required(store_id, "Store ID")

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
    def validate_status(status: str) -> str:
        InventoryItemValidator.validate_required(status, "Status")

        status_lower = status.lower().strip()

        if status_lower not in InventoryItemValidator.VALID_STATUSES:
            valid_statuses = ", ".join(InventoryItemValidator.VALID_STATUSES)
            raise ValueError(f"Status must be one of: {valid_statuses}")

        return status_lower

    @staticmethod
    def validate_inventory_item_data(
        barcode: str, album_id, store_id, status: str
    ) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate barcode
        try:
            results["barcode"] = InventoryItemValidator.validate_barcode(barcode)
        except ValueError as e:
            errors.append(str(e))

        # Validate album_id
        try:
            results["album_id"] = InventoryItemValidator.validate_album_id(album_id)
        except ValueError as e:
            errors.append(str(e))

        # Validate store_id
        try:
            results["store_id"] = InventoryItemValidator.validate_store_id(store_id)
        except ValueError as e:
            errors.append(str(e))

        # Validate status
        try:
            results["status"] = InventoryItemValidator.validate_status(status)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
