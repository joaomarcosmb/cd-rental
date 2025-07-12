from uuid import uuid4
from sqlalchemy import Column, Uuid, Enum
from sqlalchemy.orm import relationship
from models.base import BaseModel
from validators import CdStatusValidator, ValidationError


class CdStatus(BaseModel):
    __tablename__ = "cd_statuses"

    VALID_STATUSES = ["available", "rented", "maintenance", "damaged", "lost"]
    VALID_STATUSES_ENUM = Enum(*VALID_STATUSES, name="cd_status_enum")

    id = Column(Uuid, primary_key=True, default=uuid4)
    description = Column(VALID_STATUSES_ENUM, nullable=False, unique=True)

    # Relationships
    cds = relationship("Cd", back_populates="status", lazy="dynamic")

    def __init__(self, description):
        try:
            validated_data = CdStatusValidator.validate_cd_status_data(description)

            self.description = validated_data["description"]

        except ValidationError as e:
            # Convert ValidationError to ValueError for backward compatibility
            raise ValueError(str(e))

    def __repr__(self):
        return f"<CdStatus {self.description}>"
