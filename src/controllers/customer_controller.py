from flask import jsonify, request
from src.controllers.base_controller import BaseController
from src.models.customer import Customer
from src.models.person import Person


class CustomerController(BaseController):
    def __init__(self):
        super().__init__(Customer)

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
                # Check if person is already a customer
                existing_customer = Customer.query.filter_by(
                    person_id=data["person_id"]
                ).first()
                if existing_customer:
                    errors.append("Person is already a customer")

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
                    # Check if person is already a customer (excluding current customer)
                    existing_customer = Customer.query.filter_by(
                        person_id=data["person_id"]
                    ).first()
                    if (
                        existing_customer
                        and existing_customer.person_id != item.person_id
                    ):
                        errors.append("Person is already a customer")

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

            # Create new customer
            customer = Customer(person_id=data["person_id"])

            # Add to database
            customer.save()

            return jsonify(customer.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def update(self, customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return jsonify({"error": "Customer not found"}), 404

            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Validate data
            validation = self._validate_update_data(data, customer)
            if not validation["valid"]:
                return (
                    jsonify(
                        {"error": "Validation failed", "details": validation["errors"]}
                    ),
                    400,
                )

            # Update customer
            if "person_id" in data:
                customer.person_id = data["person_id"]

            customer.save()

            return jsonify(customer.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def get_all(self):
        try:
            # Get all customers with their person data
            customers = Customer.query.join(Person).all()
            return jsonify([customer.to_dict() for customer in customers]), 200
        except Exception as e:
            return jsonify({"error": "Database error occurred", "details": str(e)}), 500

    def get_by_id(self, customer_id):
        try:
            # Get customer with person data
            customer = (
                Customer.query.join(Person).filter_by(person_id=customer_id).first()
            )
            if not customer:
                return jsonify({"error": "Customer not found"}), 404
            return jsonify(customer.to_dict()), 200
        except Exception as e:
            return jsonify({"error": "Database error occurred", "details": str(e)}), 500
