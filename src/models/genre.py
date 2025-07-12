from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Genre(BaseModel):
    __tablename__ = 'genres'

    id = Column(Uuid, primary_key=True, default=uuid4)
    description = Column(String(50), nullable=False, unique=True)

    # Relationships
    cds = relationship('Cd', back_populates='genre', lazy='dynamic')

    __table_args__ = (
        CheckConstraint('length(description) >= 2', name='check_genre_description_length'),
    )

    def __init__(self, description):
        self.description = self._validate_description(description)

    def _validate_description(self, description):
        if not description or len(description.strip()) < 2:
            raise ValueError('Genre description must be at least 2 characters')
        
        return description.strip().title()

    def __repr__(self):
        return f"<Genre {self.description}>" 