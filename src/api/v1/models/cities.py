from marshmallow import fields, validate
from api.v1.models.marshmallow_init import ma

class CitySchema(ma.Schema):
    name = fields.Str(validate=validate.Length(max=100))
    country = fields.Str(validate=validate.Length(max=100))


class CityInfo(ma.Schema):
    name = fields.Str(validate=validate.Length(max=100))
    country = fields.Str(validate=validate.Length(max=100))
    lat = fields.Float()
    lon = fields.Float()


class MapPoint(ma.Schema):
    lat = fields.Float()
    lon = fields.Float()


city_schema = CitySchema()
city_info = CityInfo()
cities_list = CityInfo(many=True)
map_point = MapPoint()

