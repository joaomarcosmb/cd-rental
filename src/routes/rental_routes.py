from flask import Blueprint
from src.controllers.rental_controller import RentalController

rental_bp = Blueprint("rental", __name__)
rental_controller = RentalController()


@rental_bp.route("", methods=["GET"])
def get_all_rentals():
    """Get all rentals."""
    return rental_controller.get_all()


@rental_bp.route("/<uuid:rental_id>", methods=["GET"])
def get_rental_by_id(rental_id):
    """Get rental by ID."""
    return rental_controller.get_by_id(rental_id)


@rental_bp.route("", methods=["POST"])
def create_rental():
    """Create a new rental."""
    return rental_controller.create()


@rental_bp.route("/<uuid:rental_id>", methods=["PUT"])
def update_rental(rental_id):
    """Update rental by ID."""
    return rental_controller.update(rental_id)


@rental_bp.route("/<uuid:rental_id>", methods=["DELETE"])
def delete_rental(rental_id):
    """Delete rental by ID."""
    return rental_controller.delete(rental_id)


@rental_bp.route("/<uuid:rental_id>/return", methods=["POST"])
def return_rental(rental_id):
    """Return a rental."""
    return rental_controller.return_rental(rental_id)


@rental_bp.route("/active", methods=["GET"])
def get_active_rentals():
    """Get all active rentals."""
    return rental_controller.get_active_rentals()


@rental_bp.route("/returned", methods=["GET"])
def get_returned_rentals():
    """Get all returned rentals."""
    return rental_controller.get_returned_rentals()
