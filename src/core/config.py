from pydantic import BaseSettings, Field, PostgresDsn
# from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class PostgresConfig(BaseSettings):
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    database: str = Field(..., env='POSTGRES_DB')
    host_local: str = Field(..., env='DB_HOST_LOCAL')

    class Config:
        env_file = ".env"

pg_conf = PostgresConfig()


class AppConfig(BaseSettings):
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    SQLALCHEMY_DATABASE_URI: PostgresDsn = \
        f'postgresql://{pg_conf.user}:{pg_conf.password}@{pg_conf.host}:{pg_conf.port}/{pg_conf.database}'

class CityConfig(BaseSettings):
    api_key: str = Field(..., env='API_KEY')
    api_url: str = 'https://api.api-ninjas.com/v1/geocoding?'

app_config = AppConfig()
city_config = CityConfig()
