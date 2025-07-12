from uuid import uuid4
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, Uuid, ForeignKey, DateTime, Numeric, Enum
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Payment(BaseModel):
    __tablename__ = 'payments'

    VALID_PAYMENT_METHODS = ['cash', 'credit_card', 'debit_card', 'pix']
    VALID_STATUSES = ['pending', 'completed', 'failed', 'refunded']
    VALID_PAYMENT_METHODS_ENUM = Enum(*VALID_PAYMENT_METHODS, name='payment_method_enum')
    VALID_STATUSES_ENUM = Enum(*VALID_STATUSES, name='status_enum')

    id = Column(Uuid, primary_key=True, default=uuid4)
    rental_id = Column(Uuid, ForeignKey('rentals.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    payment_method = Column(VALID_PAYMENT_METHODS_ENUM, nullable=False)
    status = Column(VALID_STATUSES_ENUM, nullable=False)

    # Relationships
    rental = relationship('Rental', back_populates='payments')

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_payment_amount_positive'),
    )

    def __init__(self, rental_id, amount, payment_method, status='pending', payment_date=None):
        self.rental_id = rental_id
        self.amount = self._validate_amount(amount)
        self.payment_method = self._validate_payment_method(payment_method)
        self.status = self._validate_status(status)
        if payment_date:
            self.payment_date = payment_date

    def _validate_amount(self, amount):
        if not amount:
            raise ValueError('Amount is required')
        
        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal <= 0:
                raise ValueError('Amount must be positive')
            return amount_decimal
        except (ValueError, TypeError):
            raise ValueError('Amount must be a valid number')

    def _validate_payment_method(self, payment_method):
        if not payment_method:
            raise ValueError('Payment method is required')
        
        method = payment_method.lower().strip()
        if method not in self.VALID_PAYMENT_METHODS:
            raise ValueError(f'Payment method must be one of: {", ".join(self.VALID_PAYMENT_METHODS)}')
        
        return method

    def _validate_status(self, status):
        if not status:
            raise ValueError('Status is required')
        
        status_lower = status.lower().strip()
        if status_lower not in self.VALID_STATUSES:
            raise ValueError(f'Status must be one of: {", ".join(self.VALID_STATUSES)}')
        
        return status_lower

    def is_completed(self):
        return self.status == 'completed'

    def mark_as_completed(self):
        self.status = 'completed'

    def mark_as_failed(self):
        self.status = 'failed'

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        
        # Convert Decimal to float for JSON serialization
        if 'amount' in data and data['amount'] is not None:
            data['amount'] = float(data['amount'])
        
        return data

    def __repr__(self):
        return f"<Payment {self.payment_method} - R$ {self.amount} ({self.status})>" 