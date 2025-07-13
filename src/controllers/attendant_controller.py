from flask import request
from src.controllers.base_controller import BaseController
from src.models.attendant import Attendant
from src.models.person import Person
from src.models.store import Store
from src.validators.person_validator import PersonValidator


class AttendantController(BaseController):
    def __init__(self):
        super().__init__(Attendant)

    def _validate_create_data(self, data):
        errors = []

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
                return {"error": "No data provided"}, 400

            # Validate data
            validation = self._validate_create_data(data)
            if not validation["valid"]:
                return {
                    "error": "Validation failed",
                    "details": validation["errors"],
                }, 400

            # Create person
            person = Person(
                cpf=data.get("cpf"),
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
            )

            # Add person to database
            person.save()

            # Create attendant
            attendant = Attendant(person_id=person.id, store_id=data["store_id"])

            # Add attendant to database
            attendant.save()

            return attendant.to_dict(), 201
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def update(self, attendant_id):
        try:
            attendant = Attendant.query.get(attendant_id)
            if not attendant:
                return {"error": "Attendant not found"}, 404

            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Validate data
            validation = self._validate_update_data(data, attendant)
            if not validation["valid"]:
                return {
                    "error": "Validation failed",
                    "details": validation["errors"],
                }, 400

            # Update person data if provided
            person = Person.query.get(attendant.person_id)
            if not person:
                return {"error": "Person not found"}, 404

            if "cpf" in data:
                person.cpf = PersonValidator.validate_cpf(data["cpf"])
            if "name" in data:
                person.name = PersonValidator.validate_name(data["name"])
            if "phone" in data:
                person.phone = PersonValidator.validate_phone(data["phone"])
            if "email" in data:
                person.email = PersonValidator.validate_email(data["email"])

            person.save()

            # Update attendant data
            if "store_id" in data:
                attendant.store_id = data["store_id"]

            attendant.save()

            return attendant.to_dict(), 200
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def get_all(self):
        try:
            # Get all attendants with their person data
            attendants = Attendant.query.join(Person).all()
            return [attendant.to_dict() for attendant in attendants]
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def get_by_id(self, attendant_id):
        try:
            # Get attendant with person data
            attendant = (
                Attendant.query.join(Person).filter_by(person_id=attendant_id).first()
            )
            if not attendant:
                return {"error": "Attendant not found"}, 404
            return attendant.to_dict()
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def delete(self, attendant_id):
        try:
            attendant = Attendant.query.get(attendant_id)
            if not attendant:
                return {"error": "Attendant not found"}, 404

            # Get the person associated with this attendant
            person = Person.query.get(attendant.person_id)

            # Delete the person
            if person:
                person.delete()

            return {"message": "Attendant deleted successfully"}, 200
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500
