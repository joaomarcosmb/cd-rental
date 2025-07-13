from flask import Blueprint
from src.controllers.payment_controller import PaymentController

payment_bp = Blueprint("payment", __name__)
payment_controller = PaymentController()


@payment_bp.route("", methods=["GET"])
def get_all_payments():
    """Get all payments."""
    return payment_controller.get_all()


@payment_bp.route("/<uuid:payment_id>", methods=["GET"])
def get_payment_by_id(payment_id):
    """Get payment by ID."""
    return payment_controller.get_by_id(payment_id)


@payment_bp.route("", methods=["POST"])
def create_payment():
    """Create a new payment."""
    return payment_controller.create()


@payment_bp.route("/<uuid:payment_id>", methods=["PUT"])
def update_payment(payment_id):
    """Update payment by ID."""
    return payment_controller.update(payment_id)


@payment_bp.route("/<uuid:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    """Delete payment by ID."""
    return payment_controller.delete(payment_id)


@payment_bp.route("/<uuid:payment_id>/complete", methods=["POST"])
def complete_payment(payment_id):
    """Mark payment as completed."""
    return payment_controller.complete_payment(payment_id)


@payment_bp.route("/<uuid:payment_id>/fail", methods=["POST"])
def fail_payment(payment_id):
    """Mark payment as failed."""
    return payment_controller.fail_payment(payment_id)


@payment_bp.route("/status/<string:status>", methods=["GET"])
def get_payments_by_status(status):
    """Get payments by status."""
    return payment_controller.get_payments_by_status(status)


@payment_bp.route("/method/<string:method>", methods=["GET"])
def get_payments_by_method(method):
    """Get payments by payment method."""
    return payment_controller.get_payments_by_method(method)
