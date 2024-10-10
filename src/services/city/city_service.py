import requests
from core.config import city_config
from db.queries.cities import create_city, get_city_by_name, get_cities, delete_city_data


class CityAlreadyExists(Exception):
    ...


class GettingCityInfoFailed(Exception):
    ...


class CityNotFound(Exception):
    ...


def add_new_city(city: dict):
    name, country = city['name'], city['country']
    if get_city_by_name(name, country):
        raise CityAlreadyExists(f"City {name} in {country} already in db")

    response = requests.get(
        city_config.api_url + f"city={name}&country={country}",
        headers={'X-Api-Key': city_config.api_key})

    if response.status_code != requests.codes.ok:
        raise GettingCityInfoFailed("Getting info failed")

    data = response.json()[0]
    create_city({'name': name, 'country': country, 'lat': data['latitude'], 'lon': data['longitude']})


def get_all_cities():
    return get_cities()


def get_city_info(name: str, country: str):
    city = get_city_by_name(name, country)
    if not city:
        raise CityNotFound(f"City {name} in {country} not found in db")

    return city


def city_delete(name: str, country: str):
    city = get_city_info(name, country)
    delete_city_data(city)
