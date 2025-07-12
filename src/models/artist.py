from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Artist(BaseModel):
    __tablename__ = 'artists'

    id = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    cds = relationship('Cd', back_populates='artist', lazy='dynamic')

    __table_args__ = (
        CheckConstraint('length(name) >= 2', name='check_artist_name_length'),
    )

    def __init__(self, name):
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Artist name must be at least 2 characters')
        
        return name.strip().title()

    def __repr__(self):
        return f"<Artist {self.name}>" 