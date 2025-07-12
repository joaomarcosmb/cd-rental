import re
from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Store(BaseModel):
    __tablename__ = 'stores'

    id = Column(Uuid, primary_key=True, default=uuid4)
    cnpj = Column(String(14), nullable=False, unique=True)
    trade_name = Column(String(100), nullable=False)

    # Relationships
    attendants = relationship('Attendant', back_populates='store', lazy='dynamic')
    address = relationship('Address', back_populates='store', uselist=False)
    cds = relationship('Cd', back_populates='store', lazy='dynamic')

    __table_args__ = (
        CheckConstraint('length(cnpj) = 14', name='check_cnpj_length'),
        CheckConstraint('length(trade_name) >= 2', name='check_trade_name_length'),
    )

    def __init__(self, cnpj, trade_name):
        self.cnpj = self._validate_cnpj(cnpj)
        self.trade_name = self._validate_trade_name(trade_name)

    def _validate_cnpj(self, cnpj):
        if not cnpj:
            raise ValueError('CNPJ is required')

        cnpj_clean = re.sub(r'[^0-9]', '', cnpj)

        if len(cnpj_clean) != 14:
            raise ValueError('CNPJ must be 14 digits')
        
        if not cnpj_clean.isdigit():
            raise ValueError('CNPJ must be a number')
        
        if cnpj_clean == cnpj_clean[0] * 14:
            raise ValueError('CNPJ cannot have all the same digits')
        
        return cnpj_clean

    def _validate_trade_name(self, trade_name):
        if not trade_name or len(trade_name.strip()) < 2:
            raise ValueError('Trade name must be at least 2 characters')
        
        return trade_name.strip().title()

    def format_cnpj(self):
        cnpj_str = str(self.cnpj)
        if len(cnpj_str) == 14:
            return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:]}"
        
        return cnpj_str

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        data['cnpj'] = self.format_cnpj()
        return data

    def __repr__(self):
        return f"<Store {self.trade_name} - {self.cnpj}>" 