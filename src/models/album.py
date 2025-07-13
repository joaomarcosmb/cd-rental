from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid, Numeric
from sqlalchemy.orm import relationship
from .base import BaseModel
from validators import AlbumValidator, ValidationError


class Album(BaseModel):
    __tablename__ = "albums"

    id = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    rental_price = Column(Numeric(10, 2), nullable=False)
    artist = Column(String(200), nullable=False)
    genre = Column(String(200), nullable=False)

    # Relationships
    inventory_items = relationship(
        "InventoryItem", back_populates="album", lazy="dynamic"
    )

    __table_args__ = (
        CheckConstraint("length(title) >= 2", name="check_album_title_length"),
        CheckConstraint("rental_price > 0", name="check_rental_price_positive"),
    )

    def __init__(self, title, rental_price, artist, genre):
        try:
            validated_data = AlbumValidator.validate_album_data(
                title, rental_price, artist, genre
            )

            self.title = validated_data["title"]
            self.rental_price = validated_data["rental_price"]
            self.artist = validated_data["artist"]
            self.genre = validated_data["genre"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)

        # Convert Decimal to float for JSON serialization
        if "rental_price" in data and data["rental_price"] is not None:
            data["rental_price"] = float(data["rental_price"])

        return data

    def __repr__(self):
        return f"<Album {self.title} - R$ {self.rental_price}>"
