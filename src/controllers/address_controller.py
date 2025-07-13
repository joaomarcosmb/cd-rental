import re
from flask import jsonify, request
from src.controllers.base_controller import BaseController
from src.models.address import Address


class AddressController(BaseController):
    def __init__(self):
        super().__init__(Address)

    def _validate_create_data(self, data):
        errors = []

        # Validate street
        if not data.get("street"):
            errors.append("Street is required")
        elif len(data["street"].strip()) < 2:
            errors.append("Street must be at least 2 characters")

        # Validate number
        if not data.get("number"):
            errors.append("Number is required")
        elif len(str(data["number"]).strip()) < 1:
            errors.append("Number is required")

        # Validate neighborhood
        if not data.get("neighborhood"):
            errors.append("Neighborhood is required")
        elif len(data["neighborhood"].strip()) < 2:
            errors.append("Neighborhood must be at least 2 characters")

        # Validate city
        if not data.get("city"):
            errors.append("City is required")
        elif len(data["city"].strip()) < 2:
            errors.append("City must be at least 2 characters")

        # Validate state
        if not data.get("state"):
            errors.append("State is required")
        elif len(data["state"].strip()) != 2:
            errors.append("State must be 2 characters")

        # Validate ZIP code
        if not data.get("zip_code"):
            errors.append("ZIP code is required")
        else:
            try:
                zip_clean = re.sub(r"[^0-9]", "", data["zip_code"])
                if len(zip_clean) != 8:
                    errors.append("ZIP code must be 8 digits")
            except:
                errors.append("Invalid ZIP code format")

        # Validate store_id
        if not data.get("store_id"):
            errors.append("Store ID is required")

        # Validate customer_id
        if not data.get("customer_id"):
            errors.append("Customer ID is required")

        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_update_data(self, data, item):
        errors = []

        # Validate street if provided
        if "street" in data:
            if not data["street"]:
                errors.append("Street is required")
            elif len(data["street"].strip()) < 2:
                errors.append("Street must be at least 2 characters")

        # Validate number if provided
        if "number" in data:
            if not data["number"]:
                errors.append("Number is required")
            elif len(str(data["number"]).strip()) < 1:
                errors.append("Number is required")

        # Validate neighborhood if provided
        if "neighborhood" in data:
            if not data["neighborhood"]:
                errors.append("Neighborhood is required")
            elif len(data["neighborhood"].strip()) < 2:
                errors.append("Neighborhood must be at least 2 characters")

        # Validate city if provided
        if "city" in data:
            if not data["city"]:
                errors.append("City is required")
            elif len(data["city"].strip()) < 2:
                errors.append("City must be at least 2 characters")

        # Validate state if provided
        if "state" in data:
            if not data["state"]:
                errors.append("State is required")
            elif len(data["state"].strip()) != 2:
                errors.append("State must be 2 characters")

        # Validate ZIP code if provided
        if "zip_code" in data:
            if not data["zip_code"]:
                errors.append("ZIP code is required")
            else:
                try:
                    zip_clean = re.sub(r"[^0-9]", "", data["zip_code"])
                    if len(zip_clean) != 8:
                        errors.append("ZIP code must be 8 digits")
                except:
                    errors.append("Invalid ZIP code format")

        # Validate store_id if provided
        if "store_id" in data:
            if not data["store_id"]:
                errors.append("Store ID is required")

        # Validate customer_id if provided
        if "customer_id" in data:
            if not data["customer_id"]:
                errors.append("Customer ID is required")

        return {"valid": len(errors) == 0, "errors": errors}

    def create(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Validate data
            validation = self._validate_create_data(data)
            if not validation["valid"]:
                return (
                    jsonify(
                        {"error": "Validation failed", "details": validation["errors"]}
                    ),
                    400,
                )

            # Create new address
            address = Address(
                street=data["street"],
                number=data["number"],
                neighborhood=data["neighborhood"],
                city=data["city"],
                state=data["state"],
                zip_code=data["zip_code"],
                store_id=data["store_id"],
                customer_id=data["customer_id"],
            )

            # Add to database
            address.save()

            return jsonify(address.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def update(self, address_id):
        try:
            address = Address.query.get(address_id)
            if not address:
                return jsonify({"error": "Address not found"}), 404

            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Validate data
            validation = self._validate_update_data(data, address)
            if not validation["valid"]:
                return (
                    jsonify(
                        {"error": "Validation failed", "details": validation["errors"]}
                    ),
                    400,
                )

            # Update address
            if "street" in data:
                address.street = address._validate_street(data["street"])
            if "number" in data:
                address.number = address._validate_number(data["number"])
            if "neighborhood" in data:
                address.neighborhood = address._validate_neighborhood(
                    data["neighborhood"]
                )
            if "city" in data:
                address.city = address._validate_city(data["city"])
            if "state" in data:
                address.state = address._validate_state(data["state"])
            if "zip_code" in data:
                address.zip_code = address._validate_zip_code(data["zip_code"])
            if "store_id" in data:
                address.store_id = data["store_id"]
            if "customer_id" in data:
                address.customer_id = data["customer_id"]

            address.save()

            return jsonify(address.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500
