from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import Column, Uuid, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Rental(BaseModel):
    __tablename__ = 'rentals'

    id = Column(Uuid, primary_key=True, default=uuid4)
    customer_id = Column(Uuid, ForeignKey('customers.person_id'), nullable=False)
    cd_id = Column(Uuid, ForeignKey('cds.id'), nullable=False)
    attendant_id = Column(Uuid, ForeignKey('attendants.person_id'), nullable=False)
    rental_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    return_date = Column(DateTime, nullable=True)

    # Relationships
    customer = relationship('Customer', back_populates='rentals')
    cd = relationship('Cd', back_populates='rentals')
    attendant = relationship('Attendant', back_populates='rentals')
    payments = relationship('Payment', back_populates='rental', lazy='dynamic')

    def __init__(self, customer_id, cd_id, attendant_id, rental_date=None, return_date=None):
        self.customer_id = customer_id
        self.cd_id = cd_id
        self.attendant_id = attendant_id
        if rental_date:
            self.rental_date = rental_date
        if return_date:
            self.return_date = return_date

    def is_returned(self):
        return self.return_date is not None

    def mark_as_returned(self):
        if self.return_date is None:
            self.return_date = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<Rental {self.id} - Customer:{self.customer_id} CD:{self.cd_id} Attendant:{self.attendant_id}>" 