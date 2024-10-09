import uuid

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

from db.pg_db import db


class City(db.Model):
    __tablename__ = 'cities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    lat = Column(Float)
    lon = Column(Float)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
