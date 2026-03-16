from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = "LOCAL"

    # WB API
    WB_API_TOKEN: str = ""

    # Базовые хосты (у WB разные хосты для разных разделов)
    WB_API_BASE_URL: str = "https://common-api.wildberries.ru"
    WB_PRICES_URL: str = "https://discounts-prices-api.wildberries.ru"
    WB_CONTENT_URL: str = "https://content-api.wildberries.ru"
    WB_STATS_URL: str = "https://statistics-api.wildberries.ru"
    WB_ANALYTICS_URL: str = "https://seller-analytics-api.wildberries.ru"
    WB_FINANCE_URL: str = "https://finance-api.wildberries.ru"
    WB_MARKETPLACE_URL: str = "https://marketplace-api.wildberries.ru"
    WB_ADVERT_URL: str = "https://advert-api.wildberries.ru"
    WB_USER_MGMT_URL: str = "https://user-management-api.wildberries.ru"

    # PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "wb_user"
    DB_PASS: str = "wb_pass"
    DB_NAME: str = "wb_collector"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore",
    )


settings = Settings()
