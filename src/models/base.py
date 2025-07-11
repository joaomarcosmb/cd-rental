from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from config.database import db

class BaseModel(db.Model):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []

        data = {}
        for column in self.__table__.columns:  # type: ignore
            if column.name not in exclude_fields:
                value = getattr(self, column.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                data[column.name] = value

        return data

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {getattr(self, "id", "")}>'