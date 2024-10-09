from marshmallow import Schema, fields, validate
from api.v1.models.marshmallow_init import ma

class CitySchema(Schema):
    name = fields.Str(validate=validate.Length(max=100))


class CityInfo(Schema):
    name = fields.Str(validate=validate.Length(max=100))
    lat = fields.Float()
    lon = fields.Float()


city_schema = CitySchema()
city_info = CityInfo()

