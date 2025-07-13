from flask import Blueprint
from src.controllers.customer_controller import CustomerController

customer_bp = Blueprint("customer", __name__)
customer_controller = CustomerController()


@customer_bp.route("", methods=["GET"])
def get_all_customers():
    """Get all customers."""
    return customer_controller.get_all()


@customer_bp.route("/<uuid:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """Get customer by ID."""
    return customer_controller.get_by_id(customer_id)


@customer_bp.route("", methods=["POST"])
def create_customer():
    """Create a new customer."""
    return customer_controller.create()


@customer_bp.route("/<uuid:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Update customer by ID."""
    return customer_controller.update(customer_id)


@customer_bp.route("/<uuid:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Delete customer by ID."""
    return customer_controller.delete(customer_id)
