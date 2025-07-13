from flask import request
from src.controllers.base_controller import BaseController
from src.models.customer import Customer
from src.models.person import Person
from src.validators.person_validator import PersonValidator


class CustomerController(BaseController):
    def __init__(self):
        super().__init__(Customer)

    def create(self):
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            # Create person
            person = Person(
                cpf=data.get("cpf"),
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
            )

            # Add to database
            person.save()

            # Create customer
            customer = Customer(person_id=person.id)

            # Add to database
            customer.save()

            return person.to_dict(), 201
        except ValueError as e:
            return {"error": "Invalid data provided", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def update(self, customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return {"error": "Customer not found"}, 404

            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            person = Person.query.get(customer.person_id)
            if not person:
                return {"error": "Person not found"}, 404

            # Update person
            if "cpf" in data:
                person.cpf = PersonValidator.validate_cpf(data["cpf"])
            if "name" in data:
                person.name = PersonValidator.validate_name(data["name"])
            if "phone" in data:
                person.phone = PersonValidator.validate_phone(data["phone"])
            if "email" in data:
                person.email = PersonValidator.validate_email(data["email"])

            person.save()

            return person.to_dict(), 200
        except ValueError as e:
            return {"error": "Validation failed", "details": str(e)}, 400
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500

    def get_all(self):
        try:
            # Get all customers with their person data
            customers = Customer.query.join(Person).all()
            return [customer.to_dict() for customer in customers]
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def get_by_id(self, customer_id):
        try:
            # Get customer with person data
            customer = (
                Customer.query.join(Person).filter_by(person_id=customer_id).first()
            )
            if not customer:
                return {"error": "Customer not found"}, 404
            return customer.to_dict()
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

    def delete(self, customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return {"error": "Customer not found"}, 404

            # Get the person associated with this customer
            person = Person.query.get(customer.person_id)

            # Delete the person if it exists
            if person:
                person.delete()

            return {"message": "Customer deleted successfully"}, 200
        except Exception as e:
            return {"error": "Database error occurred", "details": str(e)}, 500
