import re
from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from .base import BaseModel
from src.validators import StoreValidator, ValidationError


class Store(BaseModel):
    __tablename__ = "stores"

    id = Column(Uuid, primary_key=True, default=uuid4)
    cnpj = Column(String(14), nullable=False, unique=True)
    trade_name = Column(String(100), nullable=False)

    # Relationships
    attendants = relationship("Attendant", back_populates="store", lazy="dynamic")
    address = relationship("Address", back_populates="store", uselist=False)
    inventory_items = relationship("InventoryItem", back_populates="store", lazy="dynamic")

    __table_args__ = (
        CheckConstraint("length(cnpj) = 14", name="check_cnpj_length"),
        CheckConstraint("length(trade_name) >= 2", name="check_trade_name_length"),
    )

    def __init__(self, cnpj, trade_name):
        try:
            validated_data = StoreValidator.validate_store_data(cnpj, trade_name)

            self.cnpj = validated_data["cnpj"]
            self.trade_name = validated_data["trade_name"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def format_cnpj(self):
        cnpj_str = str(self.cnpj)
        if len(cnpj_str) == 14:
            return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:]}"

        return cnpj_str

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        data["cnpj"] = self.format_cnpj()
        return data

    def __repr__(self):
        return f"<Store {self.trade_name} - {self.cnpj}>"
