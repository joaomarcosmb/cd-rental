from flask import Blueprint
from src.controllers.attendant_controller import AttendantController

attendant_bp = Blueprint("attendant", __name__)
attendant_controller = AttendantController()


@attendant_bp.route("", methods=["GET"])
def get_all_attendants():
    """Get all attendants."""
    return attendant_controller.get_all()


@attendant_bp.route("/<uuid:attendant_id>", methods=["GET"])
def get_attendant_by_id(attendant_id):
    """Get attendant by ID."""
    return attendant_controller.get_by_id(attendant_id)


@attendant_bp.route("", methods=["POST"])
def create_attendant():
    """Create a new attendant."""
    return attendant_controller.create()


@attendant_bp.route("/<uuid:attendant_id>", methods=["PUT"])
def update_attendant(attendant_id):
    """Update attendant by ID."""
    return attendant_controller.update(attendant_id)


@attendant_bp.route("/<uuid:attendant_id>", methods=["DELETE"])
def delete_attendant(attendant_id):
    """Delete attendant by ID."""
    return attendant_controller.delete(attendant_id)
