from flask_restx import Namespace, Resource
from flask import request
from src.controllers.inventory_item_controller import InventoryItemController
from src.models.swagger_models import (
    inventory_item_model,
    inventory_item_input_model,
    error_model,
    success_model,
)

# Create namespace for inventory items
inventory_item_ns = Namespace(
    "inventory-items", description="Inventory item operations"
)
inventory_item_controller = InventoryItemController()


@inventory_item_ns.route("")
class InventoryItemList(Resource):
    @inventory_item_ns.doc("get_all_inventory_items")
    @inventory_item_ns.marshal_list_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", [inventory_item_model])
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all inventory items"""
        try:
            items = inventory_item_controller.get_all_inventory_items()
            return [item.to_dict() for item in items], 200
        except Exception as e:
            return {"error": str(e)}, 500

    @inventory_item_ns.doc("create_inventory_item")
    @inventory_item_ns.expect(inventory_item_input_model)
    @inventory_item_ns.response(
        201, "Inventory item created successfully", inventory_item_model
    )
    @inventory_item_ns.response(400, "Invalid input", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new inventory item"""
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            item = inventory_item_controller.create_inventory_item(
                barcode=data.get("barcode"),
                album_id=data.get("album_id"),
                store_id=data.get("store_id"),
                status=data.get("status", "available"),
            )
            return item.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/<uuid:item_id>")
@inventory_item_ns.param("item_id", "Inventory Item UUID")
class InventoryItem(Resource):
    @inventory_item_ns.doc("get_inventory_item_by_id")
    @inventory_item_ns.marshal_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", inventory_item_model)
    @inventory_item_ns.response(404, "Inventory item not found", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self, item_id):
        """Get inventory item by ID"""
        try:
            item = inventory_item_controller.get_inventory_item_by_id(item_id)
            return item.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @inventory_item_ns.doc("update_inventory_item_status")
    @inventory_item_ns.expect(inventory_item_input_model)
    @inventory_item_ns.marshal_with(inventory_item_model)
    @inventory_item_ns.response(
        200, "Inventory item updated successfully", inventory_item_model
    )
    @inventory_item_ns.response(404, "Inventory item not found", error_model)
    @inventory_item_ns.response(400, "Invalid input", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def put(self, item_id):
        """Update inventory item status"""
        try:
            data = request.get_json()
            if not data or "status" not in data:
                return {"error": "Status is required"}, 400

            item = inventory_item_controller.update_inventory_item_status(
                item_id, data["status"]
            )
            return item.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @inventory_item_ns.doc("delete_inventory_item")
    @inventory_item_ns.response(
        200, "Inventory item deleted successfully", success_model
    )
    @inventory_item_ns.response(404, "Inventory item not found", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def delete(self, item_id):
        """Delete inventory item by ID"""
        try:
            inventory_item_controller.delete_inventory_item(item_id)
            return {"message": "Inventory item deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/barcode/<string:barcode>")
@inventory_item_ns.param("barcode", "Item barcode")
class InventoryItemByBarcode(Resource):
    @inventory_item_ns.doc("get_inventory_item_by_barcode")
    @inventory_item_ns.marshal_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", inventory_item_model)
    @inventory_item_ns.response(404, "Inventory item not found", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self, barcode):
        """Get inventory item by barcode"""
        try:
            item = inventory_item_controller.get_inventory_item_by_barcode(barcode)
            return item.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/store/<uuid:store_id>")
@inventory_item_ns.param("store_id", "Store UUID")
class InventoryItemsByStore(Resource):
    @inventory_item_ns.doc("get_inventory_items_by_store")
    @inventory_item_ns.marshal_list_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", [inventory_item_model])
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self, store_id):
        """Get inventory items by store"""
        try:
            items = inventory_item_controller.get_inventory_items_by_store(store_id)
            return [item.to_dict() for item in items], 200
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/album/<uuid:album_id>")
@inventory_item_ns.param("album_id", "Album UUID")
class InventoryItemsByAlbum(Resource):
    @inventory_item_ns.doc("get_inventory_items_by_album")
    @inventory_item_ns.marshal_list_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", [inventory_item_model])
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self, album_id):
        """Get inventory items by album"""
        try:
            items = inventory_item_controller.get_inventory_items_by_album(album_id)
            return [item.to_dict() for item in items], 200
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/status/<string:status>")
@inventory_item_ns.param("status", "Item status")
class InventoryItemsByStatus(Resource):
    @inventory_item_ns.doc("get_inventory_items_by_status")
    @inventory_item_ns.marshal_list_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", [inventory_item_model])
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self, status):
        """Get inventory items by status"""
        try:
            items = inventory_item_controller.get_inventory_items_by_status(status)
            return [item.to_dict() for item in items], 200
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/available")
class AvailableInventoryItems(Resource):
    @inventory_item_ns.doc("get_available_items")
    @inventory_item_ns.param("album_id", "Filter by album UUID")
    @inventory_item_ns.param("store_id", "Filter by store UUID")
    @inventory_item_ns.marshal_list_with(inventory_item_model)
    @inventory_item_ns.response(200, "Success", [inventory_item_model])
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get available inventory items"""
        try:
            album_id = request.args.get("album_id")
            store_id = request.args.get("store_id")

            items = inventory_item_controller.get_available_items(
                album_id=album_id, store_id=store_id
            )
            return [item.to_dict() for item in items], 200
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/<uuid:item_id>/rent")
@inventory_item_ns.param("item_id", "Inventory Item UUID")
class RentInventoryItem(Resource):
    @inventory_item_ns.doc("rent_item")
    @inventory_item_ns.marshal_with(inventory_item_model)
    @inventory_item_ns.response(200, "Item rented successfully", inventory_item_model)
    @inventory_item_ns.response(400, "Invalid request", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def post(self, item_id):
        """Mark item as rented"""
        try:
            item = inventory_item_controller.rent_item(item_id)
            return item.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


@inventory_item_ns.route("/<uuid:item_id>/return")
@inventory_item_ns.param("item_id", "Inventory Item UUID")
class ReturnInventoryItem(Resource):
    @inventory_item_ns.doc("return_item")
    @inventory_item_ns.marshal_with(inventory_item_model)
    @inventory_item_ns.response(200, "Item returned successfully", inventory_item_model)
    @inventory_item_ns.response(400, "Invalid request", error_model)
    @inventory_item_ns.response(500, "Internal Server Error", error_model)
    def post(self, item_id):
        """Mark item as returned"""
        try:
            item = inventory_item_controller.return_item(item_id)
            return item.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500
