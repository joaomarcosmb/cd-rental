import re
from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from .base import BaseModel
from validators import PersonValidator, ValidationError


class Person(BaseModel):
    __tablename__ = "persons"

    id = Column(Uuid, primary_key=True, default=uuid4)
    cpf = Column(String(11), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    # Relationships
    customer = relationship("Customer", back_populates="person", uselist=False)
    attendant = relationship("Attendant", back_populates="person", uselist=False)

    __table_args__ = (
        CheckConstraint("length(cpf) = 11", name="check_person_cpf_length"),
        CheckConstraint("length(name) >= 2", name="check_person_name_length"),
        CheckConstraint('email LIKE "%@%.%"', name="check_person_email_format"),
    )

    def __init__(self, cpf, name, phone, email):
        try:
            validated_data = PersonValidator.validate_person_data(
                cpf, name, phone, email
            )

            self.cpf = validated_data["cpf"]
            self.name = validated_data["name"]
            self.phone = validated_data["phone"]
            self.email = validated_data["email"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def format_cpf(self):
        cpf_str = str(self.cpf)
        if len(cpf_str) == 11:
            return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
        return cpf_str

    def format_phone(self):
        phone_str = str(self.phone)
        if len(phone_str) == 11:
            return f"({phone_str[:2]}) 9 {phone_str[2:4]}-{phone_str[4:]}"
        return phone_str

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)

        data["cpf"] = self.format_cpf()
        data["phone"] = self.format_phone()
        return data

    def __repr__(self):
        return f"<Person {self.name} - {self.cpf}>"
