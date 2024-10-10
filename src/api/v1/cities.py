from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.v1.models.cities import city_schema, city_info, cities_list
from services.city.city_service import (
    add_new_city,
    get_all_cities,
    get_city_info,
    city_delete,
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
    name = request.args.get('name')
    country = request.args.get('country')
    try:
        city = get_city_info(name, country)
    except CityNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    result = city_info.dump(city)

    return jsonify(result)


@city_bp.route('/', methods=['DELETE'])
def delete_city():
    name = request.args.get('name')
    country = request.args.get('country')
    try:
        city_delete(name, country)
    except CityNotFound as err:
        return jsonify(message=str(err)), HTTPStatus.NOT_FOUND

    return {'message': 'City deleted successfully'}, HTTPStatus.OK

