import logging

from enum import StrEnum
from typing import Optional, Any

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

generic_config = SettingsConfigDict(env_file="../env/.app.env", extra="allow")
LOG_FORMAT_DEBUG = (
    "%(levelname)s:     %(message)s  %(pathname)s:%(funcName)s:%(lineno)d"
)


class LogLevel(StrEnum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"


class ApiConfig(BaseSettings):
    model_config = generic_config
    debug: bool = False
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    secret_key: SecretStr
    title: str = "Online shop"
    version: str = "0.0.0"
    encoding: str = "utf8"
    allowed_origins: list[str] = ["http://frontend:3000"]
    pool_size: int = 10
    pool_max_overflow: int = 0
    db_echo: bool = False
    db_dsn: str
    cache_dsn: str
    log_level_in: Optional[str] = Field(None, validation_alias="log_level")

    @property
    def log_level(self) -> str:
        if self.log_level_in:
            return self.log_level_in.lower()

        if self.debug:
            return LogLevel.debug.lower()

        return LogLevel.warning.lower()

    def configure_logging(self) -> None:
        log_level = self.log_level.upper()
        log_levels = list(LogLevel)

        if log_level not in log_levels:
            # We use LogLevel.error as the default log level
            logging.basicConfig(level=LogLevel.error)
            return

        if log_level == LogLevel.debug:
            logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
            return

        logging.basicConfig(level=log_level)


def get_migrations_config() -> ApiConfig:
    """Gets the app_config and populates the base registry with tables."""
    from container import ApplicationContainer

    config_cls: Any = type("MigrationsAppConfig", (ApiConfig,), {})
    config_cls.model_config["env_file"] = "env/.app.env"
    ApplicationContainer(config=(app_config := config_cls()))
    return app_config
