"""Сервис Sync: Общее — Синхронизация информации о продавце."""
import logging
from src.collectors.general.seller import SellerCollector
from src.schemas.general.seller import SellerInfo
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class SellerSyncService(BaseService):

    async def sync_seller_info(self) -> SellerInfo:
        async with SellerCollector() as c:
            seller = await c.get_seller_info()
        async with self.db as db:
            result = await db.seller.upsert(seller)
            await db.commit()
        logger.info(f"Seller info synced: {result.name} ({result.sid})")
        return result
