from flask import Blueprint, request, jsonify
from src.controllers.inventory_item_controller import InventoryItemController

inventory_item_bp = Blueprint("inventory_item", __name__)
inventory_item_controller = InventoryItemController()


@inventory_item_bp.route("", methods=["GET"])
def get_all_inventory_items():
    """Get all inventory items."""
    try:
        items = inventory_item_controller.get_all_inventory_items()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/<uuid:item_id>", methods=["GET"])
def get_inventory_item_by_id(item_id):
    """Get inventory item by ID."""
    try:
        item = inventory_item_controller.get_inventory_item_by_id(item_id)
        return jsonify(item.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("", methods=["POST"])
def create_inventory_item():
    """Create a new inventory item."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        item = inventory_item_controller.create_inventory_item(
            barcode=data.get("barcode"),
            album_id=data.get("album_id"),
            store_id=data.get("store_id"),
            status=data.get("status", "available"),
        )
        return jsonify(item.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/<uuid:item_id>", methods=["PUT"])
def update_inventory_item_status(item_id):
    """Update inventory item status."""
    try:
        data = request.get_json()
        if not data or "status" not in data:
            return jsonify({"error": "Status is required"}), 400

        item = inventory_item_controller.update_inventory_item_status(
            item_id, data["status"]
        )
        return jsonify(item.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/<uuid:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    """Delete inventory item by ID."""
    try:
        inventory_item_controller.delete_inventory_item(item_id)
        return jsonify({"message": "Inventory item deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/barcode/<string:barcode>", methods=["GET"])
def get_inventory_item_by_barcode(barcode):
    """Get inventory item by barcode."""
    try:
        item = inventory_item_controller.get_inventory_item_by_barcode(barcode)
        return jsonify(item.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/store/<uuid:store_id>", methods=["GET"])
def get_inventory_items_by_store(store_id):
    """Get inventory items by store."""
    try:
        items = inventory_item_controller.get_inventory_items_by_store(store_id)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/album/<uuid:album_id>", methods=["GET"])
def get_inventory_items_by_album(album_id):
    """Get inventory items by album."""
    try:
        items = inventory_item_controller.get_inventory_items_by_album(album_id)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/status/<string:status>", methods=["GET"])
def get_inventory_items_by_status(status):
    """Get inventory items by status."""
    try:
        items = inventory_item_controller.get_inventory_items_by_status(status)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/available", methods=["GET"])
def get_available_items():
    """Get available inventory items."""
    try:
        album_id = request.args.get("album_id")
        store_id = request.args.get("store_id")

        items = inventory_item_controller.get_available_items(
            album_id=album_id, store_id=store_id
        )
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/<uuid:item_id>/rent", methods=["POST"])
def rent_item(item_id):
    """Mark item as rented."""
    try:
        item = inventory_item_controller.rent_item(item_id)
        return jsonify(item.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventory_item_bp.route("/<uuid:item_id>/return", methods=["POST"])
def return_item(item_id):
    """Mark item as returned."""
    try:
        item = inventory_item_controller.return_item(item_id)
        return jsonify(item.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
