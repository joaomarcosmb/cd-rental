from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Address(BaseModel):
    __tablename__ = 'addresses'

    id = Column(Uuid, primary_key=True, default=uuid4)
    street = Column(String(200), nullable=False)
    number = Column(String(10), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(8), nullable=False)
    store_id = Column(Uuid, ForeignKey('stores.id'), nullable=False)

    # Relationships
    store = relationship('Store', back_populates='address')

    __table_args__ = (
        CheckConstraint('length(street) >= 2', name='check_street_length'),
        CheckConstraint('length(number) >= 1', name='check_number_length'),
        CheckConstraint('length(neighborhood) >= 2', name='check_neighborhood_length'),
        CheckConstraint('length(city) >= 2', name='check_city_length'),
        CheckConstraint('length(state) = 2', name='check_state_length'),
        CheckConstraint('length(zip_code) = 8', name='check_zip_code_length'),
    )

    def __init__(self, street, number, neighborhood, city, state, zip_code, store_id):
        self.street = self._validate_street(street)
        self.number = self._validate_number(number)
        self.neighborhood = self._validate_neighborhood(neighborhood)
        self.city = self._validate_city(city)
        self.state = self._validate_state(state)
        self.zip_code = self._validate_zip_code(zip_code)
        self.store_id = store_id

    def _validate_street(self, street):
        if not street or len(street.strip()) < 2:
            raise ValueError('Street must be at least 2 characters')
        
        return street.strip().title()

    def _validate_number(self, number):
        if not number or len(str(number).strip()) < 1:
            raise ValueError('Number is required')
        
        return str(number).strip()

    def _validate_neighborhood(self, neighborhood):
        if not neighborhood or len(neighborhood.strip()) < 2:
            raise ValueError('Neighborhood must be at least 2 characters')
        
        return neighborhood.strip().title()

    def _validate_city(self, city):
        if not city or len(city.strip()) < 2:
            raise ValueError('City must be at least 2 characters')
        
        return city.strip().title()

    def _validate_state(self, state):
        if not state or len(state.strip()) != 2:
            raise ValueError('State must be 2 characters')
        
        return state.strip().upper()

    def _validate_zip_code(self, zip_code):
        if not zip_code:
            raise ValueError('ZIP code is required')
        
        import re
        zip_clean = re.sub(r'[^0-9]', '', zip_code)
        
        if len(zip_clean) != 8:
            raise ValueError('ZIP code must be 8 digits')
        
        return zip_clean

    def format_zip_code(self):
        zip_str = str(self.zip_code)
        if len(zip_str) == 8:
            return f"{zip_str[:5]}-{zip_str[5:]}"
        
        return zip_str

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        data['zip_code'] = self.format_zip_code()
        return data

    def __repr__(self):
        return f"<Address {self.street}, {self.number} - {self.city}/{self.state}>" 