from flask_restx import Namespace, Resource
from flask_restx.api import HTTPStatus
from src.controllers.payment_controller import PaymentController
from src.models.swagger_models import (
    payment_model,
    payment_input_model,
    error_model,
    success_model,
)

# Create namespace for payments
payment_ns = Namespace("payments", description="Payment operations")
payment_controller = PaymentController()


@payment_ns.route("")
class PaymentList(Resource):
    @payment_ns.doc("get_all_payments")
    @payment_ns.marshal_list_with(payment_model)
    @payment_ns.response(200, "Success", [payment_model])
    @payment_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all payments"""
        return payment_controller.get_all()

    @payment_ns.doc("create_payment")
    @payment_ns.expect(payment_input_model)
    @payment_ns.marshal_with(payment_model, code=HTTPStatus.CREATED)
    @payment_ns.response(201, "Payment created successfully", payment_model)
    @payment_ns.response(400, "Invalid input", error_model)
    @payment_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new payment"""
        return payment_controller.create()


@payment_ns.route("/<uuid:payment_id>")
@payment_ns.param("payment_id", "Payment UUID")
class Payment(Resource):
    @payment_ns.doc("get_payment_by_id")
    @payment_ns.marshal_with(payment_model)
    @payment_ns.response(200, "Success", payment_model)
    @payment_ns.response(404, "Payment not found", error_model)
    @payment_ns.response(500, "Internal Server Error", error_model)
    def get(self, payment_id):
        """Get payment by ID"""
        return payment_controller.get_by_id(payment_id)

    @payment_ns.doc("update_payment")
    @payment_ns.expect(payment_input_model)
    @payment_ns.marshal_with(payment_model)
    @payment_ns.response(200, "Payment updated successfully", payment_model)
    @payment_ns.response(404, "Payment not found", error_model)
    @payment_ns.response(400, "Invalid input", error_model)
    @payment_ns.response(500, "Internal Server Error", error_model)
    def put(self, payment_id):
        """Update payment by ID"""
        return payment_controller.update(payment_id)

    @payment_ns.doc("delete_payment")
    @payment_ns.response(200, "Payment deleted successfully", success_model)
    @payment_ns.response(404, "Payment not found", error_model)
    @payment_ns.response(500, "Internal Server Error", error_model)
    def delete(self, payment_id):
        """Delete payment by ID"""
        return payment_controller.delete(payment_id)


@payment_ns.route("/<uuid:payment_id>/complete")
@payment_ns.param("payment_id", "Payment UUID")
class CompletePayment(Resource):
    @payment_ns.doc("complete_payment")
    @payment_ns.marshal_with(payment_model)
    @payment_ns.response(200, "Payment completed successfully", payment_model)
    @payment_ns.response(404, "Payment not found", error_model)
    @payment_ns.response(400, "Invalid request", error_model)
    @payment_ns.response(500, "Internal Server Error", error_model)
    def post(self, payment_id):
        """Mark payment as completed"""
        return payment_controller.complete_payment(payment_id)


@payment_ns.route("/<uuid:payment_id>/fail")
@payment_ns.param("payment_id", "Payment UUID")
class FailPayment(Resource):
    @payment_ns.doc("fail_payment")
    @payment_ns.marshal_with(payment_model)
    @payment_ns.response(200, "Payment failed successfully", payment_model)
    @payment_ns.response(404, "Payment not found", error_model)
    @payment_ns.response(400, "Invalid request", error_model)
    @payment_ns.response(500, "Internal Server Error", error_model)
    def post(self, payment_id):
        """Mark payment as failed"""
        return payment_controller.fail_payment(payment_id)


@payment_ns.route("/status/<string:status>")
@payment_ns.param("status", "Payment status")
class PaymentsByStatus(Resource):
    @payment_ns.doc("get_payments_by_status")
    @payment_ns.marshal_list_with(payment_model)
    @payment_ns.response(200, "Success", [payment_model])
    @payment_ns.response(500, "Internal Server Error", error_model)
    def get(self, status):
        """Get payments by status"""
        return payment_controller.get_payments_by_status(status)


@payment_ns.route("/method/<string:method>")
@payment_ns.param("method", "Payment method")
class PaymentsByMethod(Resource):
    @payment_ns.doc("get_payments_by_method")
    @payment_ns.marshal_list_with(payment_model)
    @payment_ns.response(200, "Success", [payment_model])
    @payment_ns.response(500, "Internal Server Error", error_model)
    def get(self, method):
        """Get payments by payment method"""
        return payment_controller.get_payments_by_method(method)
