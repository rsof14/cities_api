import requests
from core.config import city_config
from db.queries.cities import create_city, does_city_exists


class CityAlreadyExists(Exception):
    ...


class GettingCityInfoFailed(Exception):
    ...


def add_new_city(name: str):
    if does_city_exists(name):
        raise CityAlreadyExists(f'City {name} already in db')

    response = requests.get(city_config.api_url + f'city={name}',
                            headers={'X-Api-Key': city_config.api_key})
    return response.status_code
