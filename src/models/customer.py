import re
from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = 'customers'

    id = Column(Uuid, primary_key=True, default=uuid4)

    cpf = Column(String(11), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False) # +5585999999999
    email = Column(String(100), nullable=False, unique=True)

    rentals = relationship('Rental', back_populates='customer', lazy='dynamic') # lazy='dynamic' means that the rentals will be loaded only when needed

    __table_args__ = (
        CheckConstraint('length(cpf) = 11', name='check_cpf_length'),
        CheckConstraint('length(name) >= 2', name='check_name_length'),
        CheckConstraint('email LIKE "%@%.%"', name='check_email_format') # email must have @ and .
    )

    def __init__(self, cpf, name, phone, email):
        self.cpf = self._validate_cpf(cpf)
        self.name = self._validate_name(name)
        self.phone = self._validate_phone(phone)
        self.email = self._validate_email(email)

    def _validate_cpf(self, cpf):
        if not cpf:
            raise ValueError('CPF is required')

        cpf_clean = re.sub(r'[^0-9]', '', cpf) # remove all non-numeric characters

        if len(cpf_clean) != 11:
            raise ValueError('CPF must be 11 digits')
        
        if not cpf_clean.isdigit():
            raise ValueError('CPF must be a number')
        
        if cpf_clean == cpf_clean[0] * 11: # throws error if cpf has all the same digits
            raise ValueError('CPF cannot have all the same digits')
        
        return cpf_clean

    def _validate_name(self, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Name must be at least 2 characters')
        
        return name.strip().title()
    
    def _validate_phone(self, phone):
        if not phone:
            raise ValueError('Phone is required')
        
        phone_clean = re.sub(r'[^0-9]', '', phone)

        if len(phone_clean) != 11:  # 85999999999 = 11 digits
            raise ValueError('Phone must be in the format 85999999999')
        
        return phone_clean
    
    def _validate_email(self, email):
        if not email:
            raise ValueError('Email is required')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError('Email must be a valid email address')
        
        return email.strip().lower()
    
    def format_cpf(self):
        cpf_str = str(self.cpf)
        if len(cpf_str) == 11:
            return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"

        return cpf_str
    
    def format_phone(self):
        phone_str = str(self.phone)
        if len(phone_str) == 11:  # 85999999999 = 11 digits
            # returns in format (85) 9 9999-9999
            return f"({phone_str[:2]}) 9 {phone_str[2:4]}-{phone_str[4:]}"
        
        return phone_str

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        
        data['cpf'] = self.format_cpf()
        data['phone'] = self.format_phone()
        return data
    
    def __repr__(self):
        return f"<Customer {self.name} - {self.cpf}>"