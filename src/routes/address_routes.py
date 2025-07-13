from flask_restx import Namespace, Resource
from src.controllers.address_controller import AddressController
from src.models.swagger_models import (
    address_model,
    address_input_model,
    error_model,
    success_model,
)

# Create namespace for addresses
address_ns = Namespace("addresses", description="Address operations")
address_controller = AddressController()


@address_ns.route("")
class AddressList(Resource):
    @address_ns.doc("get_all_addresses")
    @address_ns.marshal_list_with(address_model)
    @address_ns.response(200, "Success", [address_model])
    @address_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all addresses"""
        return address_controller.get_all()

    @address_ns.doc("create_address")
    @address_ns.expect(address_input_model)
    @address_ns.response(201, "Address created successfully", address_model)
    @address_ns.response(400, "Invalid input", error_model)
    @address_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new address"""
        return address_controller.create()


@address_ns.route("/<uuid:address_id>")
@address_ns.param("address_id", "Address UUID")
class Address(Resource):
    @address_ns.doc("get_address_by_id")
    @address_ns.marshal_with(address_model)
    @address_ns.response(200, "Success", address_model)
    @address_ns.response(404, "Address not found", error_model)
    @address_ns.response(500, "Internal Server Error", error_model)
    def get(self, address_id):
        """Get address by ID"""
        return address_controller.get_by_id(address_id)

    @address_ns.doc("update_address")
    @address_ns.expect(address_input_model)
    @address_ns.marshal_with(address_model)
    @address_ns.response(200, "Address updated successfully", address_model)
    @address_ns.response(404, "Address not found", error_model)
    @address_ns.response(400, "Invalid input", error_model)
    @address_ns.response(500, "Internal Server Error", error_model)
    def put(self, address_id):
        """Update address by ID"""
        return address_controller.update(address_id)

    @address_ns.doc("delete_address")
    @address_ns.response(200, "Address deleted successfully", success_model)
    @address_ns.response(404, "Address not found", error_model)
    @address_ns.response(500, "Internal Server Error", error_model)
    def delete(self, address_id):
        """Delete address by ID"""
        return address_controller.delete(address_id)
