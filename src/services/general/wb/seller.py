"""Сервис WB: Общее — Информация о продавце."""
from src.collectors.general.seller import SellerCollector
from src.schemas.general.seller import SellerInfo
from src.services.base import BaseService


class SellerWbService(BaseService):

    async def ping(self) -> dict:
        async with SellerCollector() as c:
            return await c.ping()

    async def get_seller_info(self) -> SellerInfo:
        """Получает данные продавца из WB API (без сохранения в БД)."""
        async with SellerCollector() as c:
            return await c.get_seller_info()
