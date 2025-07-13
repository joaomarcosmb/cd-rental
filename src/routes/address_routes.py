from flask import Blueprint
from src.controllers.address_controller import AddressController

address_bp = Blueprint("address", __name__)
address_controller = AddressController()


@address_bp.route("", methods=["GET"])
def get_all_addresses():
    """Get all addresses."""
    return address_controller.get_all()


@address_bp.route("/<uuid:address_id>", methods=["GET"])
def get_address_by_id(address_id):
    """Get address by ID."""
    return address_controller.get_by_id(address_id)


@address_bp.route("", methods=["POST"])
def create_address():
    """Create a new address."""
    return address_controller.create()


@address_bp.route("/<uuid:address_id>", methods=["PUT"])
def update_address(address_id):
    """Update address by ID."""
    return address_controller.update(address_id)


@address_bp.route("/<uuid:address_id>", methods=["DELETE"])
def delete_address(address_id):
    """Delete address by ID."""
    return address_controller.delete(address_id)
