import logging

from src.collectors.general import GeneralCollector
from src.schemas.seller import SellerInfo
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class GeneralService(BaseService):

    async def sync_seller_info(self) -> SellerInfo:
        """
        Получить информацию о продавце из WB API и сохранить в БД.
        """
        async with GeneralCollector() as collector:
            seller = await collector.get_seller_info()

        async with self.db as db:
            result = await db.seller.upsert(seller)
            await db.commit()

        logger.info(f"Seller info synced: {result.name} ({result.sid})")
        return result

    async def ping(self) -> dict:
        """Проверка подключения к WB API."""
        async with GeneralCollector() as collector:
            return await collector.ping()
