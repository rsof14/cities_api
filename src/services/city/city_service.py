import requests
from math import radians, sin, cos, sqrt, atan2
from core.config import city_config
from db.queries.cities import (
    create_city,
    get_city_by_name,
    get_cities,
    delete_city_data,
    get_all_cities_ordered,
    get_city_by_id)


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


def get_city_info(city: dict):
    city = get_city_by_name(city['name'], city['country'])
    if not city:
        raise CityNotFound(f"City {city['name']} in {city['country']} not found in db")

    return city


def city_delete(city: dict):
    city_info = get_city_info(city)
    delete_city_data(city_info)


# Вычисление расстояния между двумя точками по широте и долготе
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# Решение перебором
def nearest_cities(point: dict):
    cities = get_all_cities()
    min1, min2 = float('inf'), float('inf')
    city1, city2 = None, None
    lat, lon = point['lat'], point['lon']
    for city in cities:
        dist = haversine(city.lat, city.lon, lat, lon)
        if dist <= min1:
            min2 = min1
            city2 = city1
            min1 = dist
            city1 = city.city_id
        elif dist <= min2:
            min2 = dist
            city2 = city.city_id

    result = []
    if city1:
        result.append(get_city_by_id(city1))
    if city2:
        result.append(get_city_by_id(city2))

    return result


# попытка эффективного решения, основанного на двоичном поиске, работает не всегда корректно
# def nearest_cities(point: dict):
#     cities = get_all_cities_ordered()
#     lat, lon = point['lat'], point['lon']
#     start, end = 0, len(cities) - 1
#     while end - start > 1:
#         mid = (end + start) // 2
#         dist1 = haversine(float(cities[mid - 1].lat), float(cities[mid - 1].lon), float(lat), float(lon))
#         dist2 = haversine(float(cities[mid + 1].lat), float(cities[mid + 1].lon), float(lat), float(lon))
#         if dist1 < dist2:
#             end = mid
#         else:
#             start = mid
#     return [cities[start], cities[end]]