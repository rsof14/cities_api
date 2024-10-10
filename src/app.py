from flask import Flask
from api.v1.models.marshmallow_init import init_marshmallow
from api.v1.cities import city_bp
from core.config import app_config
from db.pg_db import db, init_db
from db.alembic_migrate_init import init_migration_tool


def register_blueprints(app):
    API_V1_PATH = '/api/v1'
    app.register_blueprint(city_bp, url_prefix=API_V1_PATH + '/city')


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config)
    init_db(app=app)
    init_migration_tool(app=app, db=db)
    init_marshmallow(app=app)
    register_blueprints(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)