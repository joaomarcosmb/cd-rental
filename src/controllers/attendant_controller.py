from flask import jsonify, request
from src.controllers.base_controller import BaseController
from src.models.attendant import Attendant
from src.models.person import Person
from src.models.store import Store


class AttendantController(BaseController):
    def __init__(self):
        super().__init__(Attendant)

    def _validate_create_data(self, data):
        errors = []

        # Validate person_id
        if not data.get("person_id"):
            errors.append("Person ID is required")
        else:
            # Check if person exists
            person = Person.query.get(data["person_id"])
            if not person:
                errors.append("Person not found")
            else:
                # Check if person is already an attendant
                existing_attendant = Attendant.query.filter_by(
                    person_id=data["person_id"]
                ).first()
                if existing_attendant:
                    errors.append("Person is already an attendant")

        # Validate store_id
        if not data.get("store_id"):
            errors.append("Store ID is required")
        else:
            # Check if store exists
            store = Store.query.get(data["store_id"])
            if not store:
                errors.append("Store not found")

        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_update_data(self, data, item):
        errors = []

        # Validate person_id if provided
        if "person_id" in data:
            if not data["person_id"]:
                errors.append("Person ID is required")
            else:
                # Check if person exists
                person = Person.query.get(data["person_id"])
                if not person:
                    errors.append("Person not found")
                else:
                    # Check if person is already an attendant (excluding current attendant)
                    existing_attendant = Attendant.query.filter_by(
                        person_id=data["person_id"]
                    ).first()
                    if (
                        existing_attendant
                        and existing_attendant.person_id != item.person_id
                    ):
                        errors.append("Person is already an attendant")

        # Validate store_id if provided
        if "store_id" in data:
            if not data["store_id"]:
                errors.append("Store ID is required")
            else:
                # Check if store exists
                store = Store.query.get(data["store_id"])
                if not store:
                    errors.append("Store not found")

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

            # Create new attendant
            attendant = Attendant(
                person_id=data["person_id"], store_id=data["store_id"]
            )

            # Add to database
            attendant.save()

            return jsonify(attendant.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def update(self, attendant_id):
        try:
            attendant = Attendant.query.get(attendant_id)
            if not attendant:
                return jsonify({"error": "Attendant not found"}), 404

            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Validate data
            validation = self._validate_update_data(data, attendant)
            if not validation["valid"]:
                return (
                    jsonify(
                        {"error": "Validation failed", "details": validation["errors"]}
                    ),
                    400,
                )

            # Update attendant
            if "person_id" in data:
                attendant.person_id = data["person_id"]
            if "store_id" in data:
                attendant.store_id = data["store_id"]

            attendant.save()

            return jsonify(attendant.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def get_all(self):
        try:
            # Get all attendants with their person data
            attendants = Attendant.query.join(Person).all()
            return jsonify([attendant.to_dict() for attendant in attendants]), 200
        except Exception as e:
            return jsonify({"error": "Database error occurred", "details": str(e)}), 500

    def get_by_id(self, attendant_id):
        try:
            # Get attendant with person data
            attendant = (
                Attendant.query.join(Person).filter_by(person_id=attendant_id).first()
            )
            if not attendant:
                return jsonify({"error": "Attendant not found"}), 404
            return jsonify(attendant.to_dict()), 200
        except Exception as e:
            return jsonify({"error": "Database error occurred", "details": str(e)}), 500
