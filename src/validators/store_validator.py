import re
from typing import Dict
from .base_validator import BaseValidator, ValidationError


class StoreValidator(BaseValidator):
    @staticmethod
    def validate_cnpj(cnpj: str) -> str:
        StoreValidator.validate_required(cnpj, "CNPJ")

        cnpj_clean = re.sub(r"[^0-9]", "", cnpj)

        StoreValidator.validate_exact_length(cnpj_clean, 14, "CNPJ")

        if not cnpj_clean.isdigit():
            raise ValueError("CNPJ must be a number")

        if cnpj_clean == cnpj_clean[0] * 14:
            raise ValueError("CNPJ cannot have all the same digits")

        return cnpj_clean

    @staticmethod
    def validate_trade_name(trade_name: str) -> str:
        StoreValidator.validate_required(trade_name, "Trade name")
        StoreValidator.validate_min_length(trade_name, 2, "Trade name")

        return trade_name.strip().title()

    @staticmethod
    def validate_store_data(cnpj: str, trade_name: str) -> Dict[str, str]:
        errors = []
        results = {}

        # Validate CNPJ
        try:
            results["cnpj"] = StoreValidator.validate_cnpj(cnpj)
        except ValueError as e:
            errors.append(str(e))

        # Validate trade name
        try:
            results["trade_name"] = StoreValidator.validate_trade_name(trade_name)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
