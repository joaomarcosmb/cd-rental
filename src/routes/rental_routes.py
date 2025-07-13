from flask_restx import Namespace, Resource
from flask_restx.api import HTTPStatus
from src.controllers.rental_controller import RentalController
from src.models.swagger_models import (
    rental_model,
    rental_input_model,
    error_model,
    success_model,
)

# Create namespace for rentals
rental_ns = Namespace("rentals", description="Rental operations")
rental_controller = RentalController()


@rental_ns.route("")
class RentalList(Resource):
    @rental_ns.doc("get_all_rentals")
    @rental_ns.marshal_list_with(rental_model)
    @rental_ns.response(200, "Success", [rental_model])
    @rental_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all rentals"""
        return rental_controller.get_all()

    @rental_ns.doc("create_rental")
    @rental_ns.expect(rental_input_model)
    @rental_ns.marshal_with(rental_model, code=HTTPStatus.CREATED)
    @rental_ns.response(201, "Rental created successfully", rental_model)
    @rental_ns.response(400, "Invalid input", error_model)
    @rental_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new rental"""
        return rental_controller.create()


@rental_ns.route("/<uuid:rental_id>")
@rental_ns.param("rental_id", "Rental UUID")
class Rental(Resource):
    @rental_ns.doc("get_rental_by_id")
    @rental_ns.marshal_with(rental_model)
    @rental_ns.response(200, "Success", rental_model)
    @rental_ns.response(404, "Rental not found", error_model)
    @rental_ns.response(500, "Internal Server Error", error_model)
    def get(self, rental_id):
        """Get rental by ID"""
        return rental_controller.get_by_id(rental_id)

    @rental_ns.doc("update_rental")
    @rental_ns.expect(rental_input_model)
    @rental_ns.marshal_with(rental_model)
    @rental_ns.response(200, "Rental updated successfully", rental_model)
    @rental_ns.response(404, "Rental not found", error_model)
    @rental_ns.response(400, "Invalid input", error_model)
    @rental_ns.response(500, "Internal Server Error", error_model)
    def put(self, rental_id):
        """Update rental by ID"""
        return rental_controller.update(rental_id)

    @rental_ns.doc("delete_rental")
    @rental_ns.response(200, "Rental deleted successfully", success_model)
    @rental_ns.response(404, "Rental not found", error_model)
    @rental_ns.response(500, "Internal Server Error", error_model)
    def delete(self, rental_id):
        """Delete rental by ID"""
        return rental_controller.delete(rental_id)


@rental_ns.route("/<uuid:rental_id>/return")
@rental_ns.param("rental_id", "Rental UUID")
class ReturnRental(Resource):
    @rental_ns.doc("return_rental")
    @rental_ns.marshal_with(rental_model)
    @rental_ns.response(200, "Rental returned successfully", rental_model)
    @rental_ns.response(404, "Rental not found", error_model)
    @rental_ns.response(400, "Invalid request", error_model)
    @rental_ns.response(500, "Internal Server Error", error_model)
    def post(self, rental_id):
        """Return a rental"""
        return rental_controller.return_rental(rental_id)


@rental_ns.route("/active")
class ActiveRentals(Resource):
    @rental_ns.doc("get_active_rentals")
    @rental_ns.marshal_list_with(rental_model)
    @rental_ns.response(200, "Success", [rental_model])
    @rental_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all active rentals"""
        return rental_controller.get_active_rentals()


@rental_ns.route("/returned")
class ReturnedRentals(Resource):
    @rental_ns.doc("get_returned_rentals")
    @rental_ns.marshal_list_with(rental_model)
    @rental_ns.response(200, "Success", [rental_model])
    @rental_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all returned rentals"""
        return rental_controller.get_returned_rentals()
