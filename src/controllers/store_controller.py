import re
from flask import request
from src.controllers.base_controller import BaseController
from src.models.store import Store


class StoreController(BaseController):
    def __init__(self):
        super().__init__(Store)

    def _validate_create_data(self, data):
        errors = []

        # Validate CNPJ
        if not data.get("cnpj"):
            errors.append("CNPJ is required")
        else:
            try:
                cnpj_clean = re.sub(r"[^0-9]", "", data["cnpj"])
                if len(cnpj_clean) != 14:
                    errors.append("CNPJ must be 14 digits")
                elif not cnpj_clean.isdigit():
                    errors.append("CNPJ must be a number")
                elif cnpj_clean == cnpj_clean[0] * 14:
                    errors.append("CNPJ cannot have all the same digits")
            except:
                errors.append("Invalid CNPJ format")

        # Validate trade name
        if not data.get("trade_name"):
            errors.append("Trade name is required")
        elif len(data["trade_name"].strip()) < 2:
            errors.append("Trade name must be at least 2 characters")

        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_update_data(self, data, item):
        errors = []

        # Validate CNPJ if provided
        if "cnpj" in data:
            if not data["cnpj"]:
                errors.append("CNPJ is required")
            else:
                try:
                    cnpj_clean = re.sub(r"[^0-9]", "", data["cnpj"])
                    if len(cnpj_clean) != 14:
                        errors.append("CNPJ must be 14 digits")
                    elif not cnpj_clean.isdigit():
                        errors.append("CNPJ must be a number")
                    elif cnpj_clean == cnpj_clean[0] * 14:
                        errors.append("CNPJ cannot have all the same digits")
                except:
                    errors.append("Invalid CNPJ format")

        # Validate trade name if provided
        if "trade_name" in data:
            if not data["trade_name"]:
                errors.append("Trade name is required")
            elif len(data["trade_name"].strip()) < 2:
                errors.append("Trade name must be at least 2 characters")

        return {"valid": len(errors) == 0, "errors": errors}

    def create(self):
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Validate data
            validation = self._validate_create_data(data)
            if not validation["valid"]:
                return (
                    {"error": "Validation failed", "details": validation["errors"]},
                    400,
                )

            # Create new store
            store = Store(cnpj=data["cnpj"], trade_name=data["trade_name"])

            # Add to database
            store.save()

            return store.to_dict(), 201
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def update(self, store_id):
        try:
            store = Store.query.get(store_id)
            if not store:
                return {"error": "Store not found"}, 404

            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Validate data
            validation = self._validate_update_data(data, store)
            if not validation["valid"]:
                return (
                    {"error": "Validation failed", "details": validation["errors"]},
                    400,
                )

            # Update store
            if "cnpj" in data:
                store.cnpj = store._validate_cnpj(data["cnpj"])
            if "trade_name" in data:
                store.trade_name = store._validate_trade_name(data["trade_name"])

            store.save()

            return store.to_dict(), 200
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500
