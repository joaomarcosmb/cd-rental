from sqlalchemy import Column, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Customer(BaseModel):
    __tablename__ = 'customers'

    person_id = Column(Uuid, ForeignKey('persons.id'), primary_key=True)

    # Relationships
    person = relationship('Person', back_populates='customer')
    rentals = relationship('Rental', back_populates='customer', lazy='dynamic')

    def __init__(self, person_id):
        self.person_id = person_id

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        
        # Include person data if person is loaded
        if hasattr(self, 'person') and self.person:
            person_data = self.person.to_dict()
            data.update(person_data)
        
        return data
    
    def __repr__(self):
        if hasattr(self, 'person') and self.person:
            return f"<Customer {self.person.name} - {self.person.cpf}>"
        return f"<Customer {self.person_id}>"