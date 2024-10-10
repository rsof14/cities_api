import requests
from core.config import city_config
from db.queries.cities import create_city, does_city_exists


class CityAlreadyExists(Exception):
    ...


class GettingCityInfoFailed(Exception):
    ...


def add_new_city(city: dict):
    name, country = city['name'], city['country']
    if does_city_exists(name, country):
        raise CityAlreadyExists(f"City {name} in {country} already in db")

    response = requests.get(
        city_config.api_url + f"city={name}&country={country}",
        headers={'X-Api-Key': city_config.api_key})

    if response.status_code != requests.codes.ok:
        raise GettingCityInfoFailed("Getting info failed")

    data = response.json()[0]
    create_city({'name': name, 'country': country, 'lat': data['latitude'], 'lon': data['longitude']})


