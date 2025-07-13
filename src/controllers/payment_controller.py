from datetime import datetime
from flask import jsonify, request
from src.controllers.base_controller import BaseController
from src.models.payment import Payment
from src.models.rental import Rental
from src.validators import PaymentValidator, ValidationError


class PaymentController(BaseController):
    def __init__(self):
        super().__init__(Payment)

    def create(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Validate rental_id
            if not data.get("rental_id"):
                return jsonify({"error": "Rental ID is required"}), 400
            if not Rental.query.get(data["rental_id"]):
                return jsonify({"error": "Rental not found"}), 400

            # Validate payment_date if provided
            payment_date = None
            if "payment_date" in data and data["payment_date"]:
                try:
                    payment_date = datetime.fromisoformat(
                        data["payment_date"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    return (
                        jsonify(
                            {
                                "error": "Invalid payment date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                            }
                        ),
                        400,
                    )

            # Let the model handle validation
            payment = Payment(
                rental_id=data["rental_id"],
                amount=data.get("amount"),
                payment_method=data.get("payment_method"),
                status=data.get("status", "pending"),
                payment_date=payment_date,
            )

            payment.save()

            return jsonify(payment.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": "Validation failed", "details": str(e)}), 400
        except ValidationError as e:
            return jsonify({"error": "Validation failed", "details": e.errors}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def update(self, payment_id):
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Update payment using validator
            if "rental_id" in data:
                if not data["rental_id"]:
                    return jsonify({"error": "Rental ID is required"}), 400
                if not Rental.query.get(data["rental_id"]):
                    return jsonify({"error": "Rental not found"}), 400
                payment.rental_id = data["rental_id"]
            if "amount" in data:
                payment.amount = PaymentValidator.validate_amount(data["amount"])
            if "payment_method" in data:
                payment.payment_method = PaymentValidator.validate_payment_method(
                    data["payment_method"]
                )
            if "status" in data:
                payment.status = PaymentValidator.validate_status(data["status"])
            if "payment_date" in data and data["payment_date"]:
                try:
                    payment.payment_date = datetime.fromisoformat(
                        data["payment_date"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    return (
                        jsonify(
                            {
                                "error": "Invalid payment date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                            }
                        ),
                        400,
                    )

            payment.save()

            return jsonify(payment.to_dict()), 200
        except ValueError as e:
            return jsonify({"error": "Invalid data provided", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def complete_payment(self, payment_id):
        """Mark a payment as completed"""
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            if payment.is_completed():
                return jsonify({"error": "Payment already completed"}), 400

            payment.mark_as_completed()
            payment.save()

            return (
                jsonify(
                    {
                        "message": "Payment marked as completed",
                        "payment": payment.to_dict(),
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def fail_payment(self, payment_id):
        """Mark a payment as failed"""
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            payment.mark_as_failed()
            payment.save()

            return (
                jsonify(
                    {
                        "message": "Payment marked as failed",
                        "payment": payment.to_dict(),
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": "An error occurred", "details": str(e)}), 500

    def get_payments_by_status(self, status):
        """Get payments by status"""
        try:
            if status not in Payment.VALID_STATUSES:
                return (
                    jsonify(
                        {
                            "error": f'Invalid status. Must be one of: {", ".join(Payment.VALID_STATUSES)}'
                        }
                    ),
                    400,
                )

            payments = Payment.query.filter_by(status=status).all()
            return jsonify([payment.to_dict() for payment in payments]), 200
        except Exception as e:
            return jsonify({"error": "Database error occurred", "details": str(e)}), 500

    def get_payments_by_method(self, method):
        """Get payments by payment method"""
        try:
            if method not in Payment.VALID_PAYMENT_METHODS:
                return (
                    jsonify(
                        {
                            "error": f'Invalid payment method. Must be one of: {", ".join(Payment.VALID_PAYMENT_METHODS)}'
                        }
                    ),
                    400,
                )

            payments = Payment.query.filter_by(payment_method=method).all()
            return jsonify([payment.to_dict() for payment in payments]), 200
        except Exception as e:
            return jsonify({"error": "Database error occurred", "details": str(e)}), 500
