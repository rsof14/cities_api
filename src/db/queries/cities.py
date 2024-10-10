from db.models import City
from db.pg_db import db


def create_city(city: dict) -> City:
    new_city = City(**city)
    db.session.add(new_city)
    db.session.commit()
    return new_city


def does_city_exists(name: str, country: str):
    return db.session.query(City).filter(
        City.name == name, City.country == country).first()
