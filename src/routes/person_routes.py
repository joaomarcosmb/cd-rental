from flask import Blueprint
from src.controllers.person_controller import PersonController

person_bp = Blueprint("person", __name__)
person_controller = PersonController()


@person_bp.route("", methods=["GET"])
def get_all_persons():
    """Get all persons."""
    return person_controller.get_all()


@person_bp.route("/<uuid:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    """Get person by ID."""
    return person_controller.get_by_id(person_id)


@person_bp.route("", methods=["POST"])
def create_person():
    """Create a new person."""
    return person_controller.create()


@person_bp.route("/<uuid:person_id>", methods=["PUT"])
def update_person(person_id):
    """Update person by ID."""
    return person_controller.update(person_id)


@person_bp.route("/<uuid:person_id>", methods=["DELETE"])
def delete_person(person_id):
    """Delete person by ID."""
    return person_controller.delete(person_id)
