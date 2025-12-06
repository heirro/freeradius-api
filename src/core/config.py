from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal
from enum import Enum

class DatabaseType(str, Enum):
    MYSQL = "mysql"
    MARIADB = "mariadb"
    POSTGRESQL = "postgresql"

class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "freeradius-api"
    APP_DEBUG: bool = False
    
    # Database Configuration
    DB_TYPE: Literal["mysql", "mariadb", "postgresql"] = "mysql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "raduser"
    DB_PASSWORD: str = ""
    DB_NAME: str = "raddb"
    
    # Swagger UI Authentication
    SWAGGER_USERNAME: str = "admin"
    SWAGGER_PASSWORD: str = "radius"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

def get_settings() -> Settings:
    return Settings()

def get_database_url() -> str:
    settings = get_settings()
    
    if settings.DB_TYPE == "postgresql":
        # PostgreSQL connection string
        return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    else:
        # MySQL/MariaDB connection string
        return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}" 