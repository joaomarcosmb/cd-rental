from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from src.validators import AddressValidator, ValidationError


class Address(BaseModel):
    __tablename__ = "addresses"

    id = Column(Uuid, primary_key=True, default=uuid4)
    street = Column(String(200), nullable=False)
    number = Column(String(10), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(8), nullable=False)
    store_id = Column(Uuid, ForeignKey("stores.id"), nullable=False)
    customer_id = Column(Uuid, ForeignKey("customers.person_id"), nullable=False)

    # Relationships
    store = relationship("Store", back_populates="address")
    customer = relationship("Customer", back_populates="address")

    __table_args__ = (
        CheckConstraint("length(street) >= 2", name="check_street_length"),
        CheckConstraint("length(number) >= 1", name="check_number_length"),
        CheckConstraint("length(neighborhood) >= 2", name="check_neighborhood_length"),
        CheckConstraint("length(city) >= 2", name="check_city_length"),
        CheckConstraint("length(state) = 2", name="check_state_length"),
        CheckConstraint("length(zip_code) = 8", name="check_zip_code_length"),
    )

    def __init__(
        self, street, number, neighborhood, city, state, zip_code, store_id, customer_id
    ):
        try:
            validated_data = AddressValidator.validate_address_data(
                street, number, neighborhood, city, state, zip_code
            )

            self.street = validated_data["street"]
            self.number = validated_data["number"]
            self.neighborhood = validated_data["neighborhood"]
            self.city = validated_data["city"]
            self.state = validated_data["state"]
            self.zip_code = validated_data["zip_code"]
            self.store_id = store_id
            self.customer_id = customer_id

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def format_zip_code(self):
        zip_str = str(self.zip_code)
        if len(zip_str) == 8:
            return f"{zip_str[:5]}-{zip_str[5:]}"

        return zip_str

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        data["zip_code"] = self.format_zip_code()
        return data

    def __repr__(self):
        return f"<Address {self.street}, {self.number} - {self.city}/{self.state}>"
