from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.v1.models.cities import city_schema, city_info
from services.city.city_service import (add_new_city, CityAlreadyExists,
                                        GettingCityInfoFailed)


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