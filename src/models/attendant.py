from sqlalchemy import Column, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Attendant(BaseModel):
    __tablename__ = 'attendants'

    person_id = Column(Uuid, ForeignKey('persons.id'), primary_key=True)
    store_id = Column(Uuid, ForeignKey('stores.id'), nullable=False)

    # Relationships
    person = relationship('Person', back_populates='attendant')
    store = relationship('Store', back_populates='attendants')

    def __init__(self, person_id, store_id):
        self.person_id = person_id
        self.store_id = store_id

    def to_dict(self, exclude_fields=None):
        data = super().to_dict(exclude_fields)
        
        # Include person data if person is loaded
        if hasattr(self, 'person') and self.person:
            person_data = self.person.to_dict()
            data.update(person_data)
        
        return data
    
    def __repr__(self):
        if hasattr(self, 'person') and self.person:
            return f"<Attendant {self.person.name} - {self.person.cpf}>"
        return f"<Attendant {self.person_id}>" 