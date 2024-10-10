from db.models import City
from db.pg_db import db


def create_city(city: dict) -> City:
    new_city = City(**city)
    db.session.add(new_city)
    db.session.commit()
    return new_city


def get_city_by_name(name: str, country: str):
    return db.session.query(City).filter(
        City.name == name, City.country == country).first()


def get_cities():
    return City.query.all()


def delete_city_data(city):
    db.session.query(City).filter(
        City.name == city.name, City.country == city.country).delete()
    db.session.commit()


def get_all_cities_ordered():
    return City.query.order_by(City.lat, City.lon).all()


def get_city_by_id(id):
    return db.session.query(City).filter(City.city_id == id).first()