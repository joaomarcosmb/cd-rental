from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from .base import BaseModel
from validators import InventoryItemValidator, ValidationError


class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    id = Column(Uuid, primary_key=True, default=uuid4)
    album_id = Column(Uuid, ForeignKey("albums.id"), nullable=False)
    store_id = Column(Uuid, ForeignKey("stores.id"), nullable=False)
    status = Column(
        Enum("available", "rented", "maintenance", "damaged", "lost"), nullable=False
    )
    barcode = Column(String(200), nullable=False, unique=True)

    # Relationships
    album = relationship("Album", back_populates="inventory_items")
    store = relationship("Store", back_populates="inventory_items")
    rentals = relationship("Rental", back_populates="item", lazy="dynamic")

    __table_args__ = (
        CheckConstraint("length(barcode) >= 2", name="check_barcode_length"),
    )

    def __init__(self, barcode, album_id, store_id, status):
        try:
            validated_data = InventoryItemValidator.validate_inventory_item_data(
                barcode, album_id, store_id, status
            )

            self.barcode = validated_data["barcode"]
            self.album_id = validated_data["album_id"]
            self.store_id = validated_data["store_id"]
            self.status = validated_data["status"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def __repr__(self):
        return f"<InventoryItem {self.barcode} - {self.status}>"
