from flask import jsonify, request
from src.controllers.base_controller import BaseController
from src.models.person import Person
from src.validators import ValidationError, PersonValidator


class PersonController(BaseController):
    def __init__(self):
        super().__init__(Person)

    def create(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Let the model handle validation
            person = Person(
                cpf=data.get("cpf"),
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
            )

            # Add to database
            person.save()

            return jsonify(person.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": "Validation failed", "details": str(e)}), 400
        except ValidationError as e:
            return jsonify({"error": "Validation failed", "details": e.errors}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def update(self, person_id):
        try:
            person = Person.query.get(person_id)
            if not person:
                return jsonify({"error": "Person not found"}), 404

            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Update person using model validation
            if "cpf" in data:
                person.cpf = PersonValidator.validate_cpf(data["cpf"])
            if "name" in data:
                person.name = PersonValidator.validate_name(data["name"])
            if "phone" in data:
                person.phone = PersonValidator.validate_phone(data["phone"])
            if "email" in data:
                person.email = PersonValidator.validate_email(data["email"])

            person.save()

            return jsonify(person.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": "Validation failed", "details": str(e)}), 400
        except ValidationError as e:
            return jsonify({"error": "Validation failed", "details": e.errors}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500
