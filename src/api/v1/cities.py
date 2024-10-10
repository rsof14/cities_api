from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.v1.models.cities import city_schema, city_info, cities_list, map_point
from services.city.city_service import (
    add_new_city,
    get_all_cities,
    get_city_info,
    city_delete,
    nearest_cities,
    CityAlreadyExists,
    GettingCityInfoFailed,
    CityNotFound)


city_bp = Blueprint("city", __name__)

@city_bp.route('/', methods=['POST'])
def create_city():
    json_data = request.get_json()
    try:
        city = city_schema.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        add_new_city(city)
    except CityAlreadyExists as err:
        return jsonify(message=str(err)), HTTPStatus.CONFLICT
    except GettingCityInfoFailed as err:
        return jsonify(message=str(err)), HTTPStatus.BAD_REQUEST

    return {'message': 'City created'}, HTTPStatus.CREATED


@city_bp.route('/all', methods=['GET'])
def get_cities_list():
    cities = get_all_cities()
    result = cities_list.dump(cities)

    return jsonify(result)


@city_bp.route('/', methods=['GET'])
def get_city():
    json_data = request.get_json()
    try:
        city = city_schema.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        city = get_city_info(city)
    except CityNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    result = city_info.dump(city)

    return jsonify(result)


@city_bp.route('/', methods=['DELETE'])
def delete_city():
    json_data = request.get_json()
    try:
        city = city_schema.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        city_delete(city)
    except CityNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    return {'message': 'City deleted successfully'}, HTTPStatus.OK


@city_bp.route('/nearest', methods=['GET'])
def get_nearest_cities():
    json_data = request.get_json()
    try:
        point = map_point.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    cities = nearest_cities(point)

    result = cities_list.dump(cities)

    return jsonify(result)

