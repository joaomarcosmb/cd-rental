from flask import Blueprint
from src.controllers.store_controller import StoreController

store_bp = Blueprint("store", __name__)
store_controller = StoreController()


@store_bp.route("", methods=["GET"])
def get_all_stores():
    """Get all stores."""
    return store_controller.get_all()


@store_bp.route("/<uuid:store_id>", methods=["GET"])
def get_store_by_id(store_id):
    """Get store by ID."""
    return store_controller.get_by_id(store_id)


@store_bp.route("", methods=["POST"])
def create_store():
    """Create a new store."""
    return store_controller.create()


@store_bp.route("/<uuid:store_id>", methods=["PUT"])
def update_store(store_id):
    """Update store by ID."""
    return store_controller.update(store_id)


@store_bp.route("/<uuid:store_id>", methods=["DELETE"])
def delete_store(store_id):
    """Delete store by ID."""
    return store_controller.delete(store_id)
