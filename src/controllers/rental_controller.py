from datetime import datetime
from flask import request
from src.controllers.base_controller import BaseController
from src.models.rental import Rental
from src.models.customer import Customer
from src.models.inventory_item import InventoryItem
from src.models.attendant import Attendant


class RentalController(BaseController):
    def __init__(self):
        super().__init__(Rental)

    def _validate_create_data(self, data):
        errors = []

        # Validate customer_id
        if not data.get("customer_id"):
            errors.append("Customer ID is required")
        else:
            customer = Customer.query.get(data["customer_id"])
            if not customer:
                errors.append("Customer not found")

        # Validate item_id
        if not data.get("item_id"):
            errors.append("Item ID is required")
        else:
            item = InventoryItem.query.get(data["item_id"])
            if not item:
                errors.append("Inventory item not found")
            elif item.status != "available":
                errors.append("Inventory item is not available for rental")

        # Validate attendant_id
        if not data.get("attendant_id"):
            errors.append("Attendant ID is required")
        else:
            attendant = Attendant.query.get(data["attendant_id"])
            if not attendant:
                errors.append("Attendant not found")

        # Validate rental_date if provided
        if "rental_date" in data and data["rental_date"]:
            try:
                # Try to parse the date
                datetime.fromisoformat(data["rental_date"].replace("Z", "+00:00"))
            except (ValueError, TypeError):
                errors.append(
                    "Invalid rental date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )

        # Validate return_date if provided
        if "return_date" in data and data["return_date"]:
            try:
                # Try to parse the date
                return_date = datetime.fromisoformat(
                    data["return_date"].replace("Z", "+00:00")
                )

                # Check if rental_date is provided and return_date is after rental_date
                if "rental_date" in data and data["rental_date"]:
                    rental_date = datetime.fromisoformat(
                        data["rental_date"].replace("Z", "+00:00")
                    )
                    if return_date <= rental_date:
                        errors.append("Return date must be after rental date")
            except (ValueError, TypeError):
                errors.append(
                    "Invalid return date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )

        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_update_data(self, data, rental):
        errors = []

        # Validate customer_id if provided
        if "customer_id" in data:
            if not data["customer_id"]:
                errors.append("Customer ID is required")
            else:
                customer = Customer.query.get(data["customer_id"])
                if not customer:
                    errors.append("Customer not found")

        # Validate item_id if provided
        if "item_id" in data:
            if not data["item_id"]:
                errors.append("Item ID is required")
            else:
                item = InventoryItem.query.get(data["item_id"])
                if not item:
                    errors.append("Inventory item not found")
                elif item.status != "available":
                    errors.append("Inventory item is not available for rental")

        # Validate attendant_id if provided
        if "attendant_id" in data:
            if not data["attendant_id"]:
                errors.append("Attendant ID is required")
            else:
                attendant = Attendant.query.get(data["attendant_id"])
                if not attendant:
                    errors.append("Attendant not found")

        # Validate rental_date if provided
        if "rental_date" in data and data["rental_date"]:
            try:
                rental_date = datetime.fromisoformat(
                    data["rental_date"].replace("Z", "+00:00")
                )

                # Check if return_date exists and rental_date is before return_date
                if rental.return_date and rental_date >= rental.return_date:
                    errors.append("Rental date must be before return date")
            except (ValueError, TypeError):
                errors.append(
                    "Invalid rental date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )

        # Validate return_date if provided
        if "return_date" in data and data["return_date"]:
            try:
                return_date = datetime.fromisoformat(
                    data["return_date"].replace("Z", "+00:00")
                )

                # Check if return_date is after rental_date
                if return_date <= rental.rental_date:
                    errors.append("Return date must be after rental date")
            except (ValueError, TypeError):
                errors.append(
                    "Invalid return date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )

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

            # Prepare rental data
            rental_data = {
                "customer_id": data["customer_id"],
                "item_id": data["item_id"],
                "attendant_id": data["attendant_id"],
            }

            # Add rental_date if provided
            if "rental_date" in data and data["rental_date"]:
                rental_data["rental_date"] = datetime.fromisoformat(
                    data["rental_date"].replace("Z", "+00:00")
                )

            # Add return_date if provided
            if "return_date" in data and data["return_date"]:
                rental_data["return_date"] = datetime.fromisoformat(
                    data["return_date"].replace("Z", "+00:00")
                )

            # Create new rental
            rental = Rental(**rental_data)

            # Update inventory item status to "rented"
            item = InventoryItem.query.get(data["item_id"])
            if item:
                item.status = "rented"

            # Add to database
            rental.save()
            if item:
                item.save()

            return rental.to_dict(), 201
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def update(self, rental_id):
        try:
            rental = Rental.query.get(rental_id)
            if not rental:
                return {"error": "Rental not found"}, 404

            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Validate data
            validation = self._validate_update_data(data, rental)
            if not validation["valid"]:
                return (
                    {"error": "Validation failed", "details": validation["errors"]},
                    400,
                )

            # Update rental
            if "customer_id" in data:
                rental.customer_id = data["customer_id"]
            if "item_id" in data:
                rental.item_id = data["item_id"]
            if "attendant_id" in data:
                rental.attendant_id = data["attendant_id"]
            if "rental_date" in data and data["rental_date"]:
                rental.rental_date = datetime.fromisoformat(
                    data["rental_date"].replace("Z", "+00:00")
                )
            if "return_date" in data:
                if data["return_date"]:
                    rental.return_date = datetime.fromisoformat(
                        data["return_date"].replace("Z", "+00:00")
                    )
                else:
                    rental.return_date = None

            rental.save()

            return rental.to_dict(), 200
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def return_rental(self, rental_id):
        """Mark a rental as returned"""
        try:
            rental = Rental.query.get(rental_id)
            if not rental:
                return {"error": "Rental not found"}, 404

            if rental.is_returned():
                return {"error": "Rental already returned"}, 400

            # Mark rental as returned
            rental.mark_as_returned()

            # Update inventory item status back to "available"
            item = InventoryItem.query.get(rental.item_id)
            if item:
                item.status = "available"
                item.save()

            rental.save()

            return rental.to_dict(), 200
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def get_active_rentals(self):
        """Get all active (not returned) rentals"""
        try:
            active_rentals = Rental.query.filter(Rental.return_date.is_(None)).all()  # type: ignore
            return [rental.to_dict() for rental in active_rentals], 200
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def get_returned_rentals(self):
        """Get all returned rentals"""
        try:
            returned_rentals = Rental.query.filter(Rental.return_date.isnot(None)).all()  # type: ignore
            return [rental.to_dict() for rental in returned_rentals], 200
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500
