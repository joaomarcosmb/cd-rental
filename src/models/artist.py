from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel
from validators import ArtistValidator, ValidationError


class Artist(BaseModel):
    __tablename__ = "artists"

    id = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    cds = relationship("Cd", back_populates="artist", lazy="dynamic")

    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="check_artist_name_length"),
    )

    def __init__(self, name):
        try:
            validated_data = ArtistValidator.validate_artist_data(name)

            self.name = validated_data["name"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def __repr__(self):
        return f"<Artist {self.name}>"
