from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel
from validators import GenreValidator, ValidationError


class Genre(BaseModel):
    __tablename__ = "genres"

    id = Column(Uuid, primary_key=True, default=uuid4)
    description = Column(String(50), nullable=False, unique=True)

    # Relationships
    cds = relationship("Cd", back_populates="genre", lazy="dynamic")

    __table_args__ = (
        CheckConstraint(
            "length(description) >= 2", name="check_genre_description_length"
        ),
    )

    def __init__(self, description):
        try:
            validated_data = GenreValidator.validate_genre_data(description)

            self.description = validated_data["description"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def __repr__(self):
        return f"<Genre {self.description}>"
