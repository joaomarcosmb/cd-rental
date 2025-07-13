from flask_restx import Namespace, Resource
from flask_restx.api import HTTPStatus
from src.controllers.customer_controller import CustomerController
from src.models.swagger_models import (
    customer_model,
    customer_input_model,
    error_model,
    success_model,
)

# Create namespace for customers
customer_ns = Namespace("customers", description="Customer operations")
customer_controller = CustomerController()


@customer_ns.route("")
class CustomerList(Resource):
    @customer_ns.doc("get_all_customers")
    @customer_ns.marshal_list_with(customer_model)
    @customer_ns.response(200, "Success", [customer_model])
    @customer_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all customers"""
        return customer_controller.get_all()

    @customer_ns.doc("create_customer")
    @customer_ns.expect(customer_input_model)
    @customer_ns.marshal_with(customer_model, code=HTTPStatus.CREATED)
    @customer_ns.response(201, "Customer created successfully", customer_model)
    @customer_ns.response(400, "Invalid input", error_model)
    @customer_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new customer"""
        return customer_controller.create()


@customer_ns.route("/<uuid:customer_id>")
@customer_ns.param("customer_id", "Customer UUID")
class Customer(Resource):
    @customer_ns.doc("get_customer_by_id")
    @customer_ns.marshal_with(customer_model)
    @customer_ns.response(200, "Success", customer_model)
    @customer_ns.response(404, "Customer not found", error_model)
    @customer_ns.response(500, "Internal Server Error", error_model)
    def get(self, customer_id):
        """Get customer by ID"""
        return customer_controller.get_by_id(customer_id)

    @customer_ns.doc("update_customer")
    @customer_ns.expect(customer_input_model)
    @customer_ns.marshal_with(customer_model)
    @customer_ns.response(200, "Customer updated successfully", customer_model)
    @customer_ns.response(404, "Customer not found", error_model)
    @customer_ns.response(400, "Invalid input", error_model)
    @customer_ns.response(500, "Internal Server Error", error_model)
    def put(self, customer_id):
        """Update customer by ID"""
        return customer_controller.update(customer_id)

    @customer_ns.doc("delete_customer")
    @customer_ns.response(200, "Customer deleted successfully", success_model)
    @customer_ns.response(404, "Customer not found", error_model)
    @customer_ns.response(500, "Internal Server Error", error_model)
    def delete(self, customer_id):
        """Delete customer by ID"""
        return customer_controller.delete(customer_id)
