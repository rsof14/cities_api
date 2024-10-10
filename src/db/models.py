import uuid

from sqlalchemy import Column, String, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from db.pg_db import db


class City(db.Model):
    __tablename__ = 'cities'

    city_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    country = Column(String(100), nullable=False, unique=True)
    lat = Column(Float)
    lon = Column(Float)
    UniqueConstraint('name', 'country', name='unique_name_country')

    def __init__(self, name, country, lat, lon):
        self.name = name
        self.country = country
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f'{self.name} in {self.country}'
