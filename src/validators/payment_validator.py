from decimal import Decimal
from typing import Any, Dict
from .base_validator import BaseValidator, ValidationError


class PaymentValidator(BaseValidator):
    VALID_PAYMENT_METHODS = ["cash", "credit_card", "debit_card", "pix"]
    VALID_STATUSES = ["pending", "completed", "failed", "refunded"]

    @staticmethod
    def validate_amount(amount) -> Decimal:
        PaymentValidator.validate_required(amount, "Amount")

        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal <= 0:
                raise ValueError("Amount must be positive")
            return amount_decimal
        except (ValueError, TypeError):
            raise ValueError("Amount must be a valid number")

    @staticmethod
    def validate_payment_method(payment_method: str) -> str:
        PaymentValidator.validate_required(payment_method, "Payment method")

        if payment_method not in PaymentValidator.VALID_PAYMENT_METHODS:
            raise ValueError(
                f"Payment method must be one of: {', '.join(PaymentValidator.VALID_PAYMENT_METHODS)}"
            )

        return payment_method

    @staticmethod
    def validate_status(status: str) -> str:
        PaymentValidator.validate_required(status, "Status")

        if status not in PaymentValidator.VALID_STATUSES:
            raise ValueError(
                f"Status must be one of: {', '.join(PaymentValidator.VALID_STATUSES)}"
            )

        return status

    @staticmethod
    def validate_payment_data(
        amount, payment_method: str, status: str = "pending"
    ) -> Dict[str, Any]:
        errors = []
        results = {}

        # Validate amount
        try:
            results["amount"] = PaymentValidator.validate_amount(amount)
        except ValueError as e:
            errors.append(str(e))

        # Validate payment method
        try:
            results["payment_method"] = PaymentValidator.validate_payment_method(
                payment_method
            )
        except ValueError as e:
            errors.append(str(e))

        # Validate status
        try:
            results["status"] = PaymentValidator.validate_status(status)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(errors)

        return results
