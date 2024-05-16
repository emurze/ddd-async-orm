from pydantic_settings import BaseSettings

from src.config import generic_config, LogLevel, ApiConfig


class TestConfig(BaseSettings):
    model_config = generic_config
    test_title: str = "Test"
    test_log_level: str = LogLevel.info
    test_db_echo: bool = False
    test_db_dsn: str = (
        "postgresql+asyncpg://adm1:12345678@localhost:5432/learning"
    )
    test_cache_dsn: str = "redis://localhost:6379/1"


def get_test_config() -> ApiConfig:
    test_config = TestConfig()
    return ApiConfig(
        log_level=test_config.test_log_level,  # type: ignore
        title=test_config.test_title,
        db_dsn=test_config.test_db_dsn,
        db_echo=test_config.test_db_echo,
        cache_dsn=test_config.test_cache_dsn,
    )
