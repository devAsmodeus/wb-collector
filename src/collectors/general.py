"""
Коллектор: 01-general
Эндпоинты:
  GET /ping              — проверка подключения
  GET /api/v1/seller-info — информация о продавце
"""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.seller import SellerInfo


class GeneralCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_API_BASE_URL)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def ping(self) -> dict:
        """Проверка связи с WB API."""
        return await self._client.get("/ping")

    async def get_seller_info(self) -> SellerInfo:
        """Получить информацию о продавце."""
        data = await self._client.get("/api/v1/seller-info")
        return SellerInfo.model_validate(data)
