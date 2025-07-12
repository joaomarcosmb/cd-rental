from uuid import uuid4
from decimal import Decimal
from sqlalchemy import CheckConstraint, Column, String, Uuid, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Cd(BaseModel):
    __tablename__ = 'cds'

    id = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    rental_price = Column(Numeric(10, 2), nullable=False)
    artist_id = Column(Uuid, ForeignKey('artists.id'), nullable=False)
    genre_id = Column(Uuid, ForeignKey('genres.id'), nullable=False)
    status_id = Column(Uuid, ForeignKey('cd_statuses.id'), nullable=False)
    store_id = Column(Uuid, ForeignKey('stores.id'), nullable=False)

    # Relationships
    artist = relationship('Artist', back_populates='cds')
    genre = relationship('Genre', back_populates='cds')
    status = relationship('CdStatus', back_populates='cds')
    store = relationship('Store', back_populates='cds')
    rentals = relationship('Rental', back_populates='cd', lazy='dynamic')

    __table_args__ = (
        CheckConstraint('length(title) >= 2', name='check_cd_title_length'),
        CheckConstraint('rental_price > 0', name='check_rental_price_positive'),
    )

    def __init__(self, title, rental_price, artist_id, genre_id, status_id, store_id):
        self.title = self._validate_title(title)
        self.rental_price = self._validate_rental_price(rental_price)
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.status_id = status_id
        self.store_id = store_id

    def _validate_title(self, title):
        if not title or len(title.strip()) < 2:
            raise ValueError('CD title must be at least 2 characters')
        
        return title.strip().title()

    def _validate_rental_price(self, rental_price):
        if not rental_price:
            raise ValueError('Rental price is required')
        
        try:
            price = Decimal(str(rental_price))
            if price <= 0:
                raise ValueError('Rental price must be positive')
            return price
        except (ValueError, TypeError):
            raise ValueError('Rental price must be a valid number')

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        
        # Convert Decimal to float for JSON serialization
        if 'rental_price' in data and data['rental_price'] is not None:
            data['rental_price'] = float(data['rental_price'])
        
        return data

    def __repr__(self):
        return f"<Cd {self.title} - R$ {self.rental_price}>" 