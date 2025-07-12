from uuid import uuid4
from sqlalchemy import CheckConstraint, Column, String, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel


class CdStatus(BaseModel):
    __tablename__ = 'cd_statuses'

    id = Column(Uuid, primary_key=True, default=uuid4)
    description = Column(String(50), nullable=False, unique=True)

    # Relationships
    cds = relationship('Cd', back_populates='status', lazy='dynamic')

    __table_args__ = (
        CheckConstraint('length(description) >= 2', name='check_cd_status_description_length'),
    )

    def __init__(self, description):
        self.description = self._validate_description(description)

    def _validate_description(self, description):
        if not description or len(description.strip()) < 2:
            raise ValueError('CD status description must be at least 2 characters')
        
        return description.strip().title()

    def __repr__(self):
        return f"<CdStatus {self.description}>" 