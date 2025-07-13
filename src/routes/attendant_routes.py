from flask_restx import Namespace, Resource
from flask_restx.api import HTTPStatus
from src.controllers.attendant_controller import AttendantController
from src.models.swagger_models import (
    attendant_model,
    attendant_input_model,
    error_model,
    success_model,
)

# Create namespace for attendants
attendant_ns = Namespace("attendants", description="Attendant operations")
attendant_controller = AttendantController()


@attendant_ns.route("")
class AttendantList(Resource):
    @attendant_ns.doc("get_all_attendants")
    @attendant_ns.marshal_list_with(attendant_model)
    @attendant_ns.response(200, "Success", [attendant_model])
    @attendant_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all attendants"""
        return attendant_controller.get_all()

    @attendant_ns.doc("create_attendant")
    @attendant_ns.expect(attendant_input_model)
    @attendant_ns.marshal_with(attendant_model, code=HTTPStatus.CREATED)
    @attendant_ns.response(201, "Attendant created successfully", attendant_model)
    @attendant_ns.response(400, "Invalid input", error_model)
    @attendant_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new attendant"""
        return attendant_controller.create()


@attendant_ns.route("/<uuid:attendant_id>")
@attendant_ns.param("attendant_id", "Attendant UUID")
class Attendant(Resource):
    @attendant_ns.doc("get_attendant_by_id")
    @attendant_ns.marshal_with(attendant_model)
    @attendant_ns.response(200, "Success", attendant_model)
    @attendant_ns.response(404, "Attendant not found", error_model)
    @attendant_ns.response(500, "Internal Server Error", error_model)
    def get(self, attendant_id):
        """Get attendant by ID"""
        return attendant_controller.get_by_id(attendant_id)

    @attendant_ns.doc("update_attendant")
    @attendant_ns.expect(attendant_input_model)
    @attendant_ns.marshal_with(attendant_model)
    @attendant_ns.response(200, "Attendant updated successfully", attendant_model)
    @attendant_ns.response(404, "Attendant not found", error_model)
    @attendant_ns.response(400, "Invalid input", error_model)
    @attendant_ns.response(500, "Internal Server Error", error_model)
    def put(self, attendant_id):
        """Update attendant by ID"""
        return attendant_controller.update(attendant_id)

    @attendant_ns.doc("delete_attendant")
    @attendant_ns.response(200, "Attendant deleted successfully", success_model)
    @attendant_ns.response(404, "Attendant not found", error_model)
    @attendant_ns.response(500, "Internal Server Error", error_model)
    def delete(self, attendant_id):
        """Delete attendant by ID"""
        return attendant_controller.delete(attendant_id)
