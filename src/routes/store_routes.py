from flask_restx import Namespace, Resource
from flask_restx.api import HTTPStatus
from src.controllers.store_controller import StoreController
from src.models.swagger_models import (
    store_model,
    store_input_model,
    error_model,
    success_model,
)

# Create namespace for stores
store_ns = Namespace("stores", description="Store operations")
store_controller = StoreController()


@store_ns.route("")
class StoreList(Resource):
    @store_ns.doc("get_all_stores")
    @store_ns.marshal_list_with(store_model)
    @store_ns.response(200, "Success", [store_model])
    @store_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all stores"""
        return store_controller.get_all()

    @store_ns.doc("create_store")
    @store_ns.expect(store_input_model)
    @store_ns.marshal_with(store_model, code=HTTPStatus.CREATED)
    @store_ns.response(201, "Store created successfully", store_model)
    @store_ns.response(400, "Invalid input", error_model)
    @store_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new store"""
        return store_controller.create()


@store_ns.route("/<uuid:store_id>")
@store_ns.param("store_id", "Store UUID")
class Store(Resource):
    @store_ns.doc("get_store_by_id")
    @store_ns.marshal_with(store_model)
    @store_ns.response(200, "Success", store_model)
    @store_ns.response(404, "Store not found", error_model)
    @store_ns.response(500, "Internal Server Error", error_model)
    def get(self, store_id):
        """Get store by ID"""
        return store_controller.get_by_id(store_id)

    @store_ns.doc("update_store")
    @store_ns.expect(store_input_model)
    @store_ns.marshal_with(store_model)
    @store_ns.response(200, "Store updated successfully", store_model)
    @store_ns.response(404, "Store not found", error_model)
    @store_ns.response(400, "Invalid input", error_model)
    @store_ns.response(500, "Internal Server Error", error_model)
    def put(self, store_id):
        """Update store by ID"""
        return store_controller.update(store_id)

    @store_ns.doc("delete_store")
    @store_ns.response(200, "Store deleted successfully", success_model)
    @store_ns.response(404, "Store not found", error_model)
    @store_ns.response(500, "Internal Server Error", error_model)
    def delete(self, store_id):
        """Delete store by ID"""
        return store_controller.delete(store_id)
