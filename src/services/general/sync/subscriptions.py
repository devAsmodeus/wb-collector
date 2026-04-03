"""Сервис Sync: Общее — Синхронизация подписок Джем."""
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.general.subscriptions import SubscriptionsCollector
from src.repositories.general.subscriptions import SubscriptionsRepository
from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class SubscriptionsSyncService(BaseService):

    async def sync_full(self, session: AsyncSession) -> SubscriptionsJamInfo:
        """Запрашивает подписки у WB и сохраняет/обновляет в таблице wb_seller_subscriptions."""
        repo = SubscriptionsRepository(session)
        async with SubscriptionsCollector() as c:
            subscription = await c.get_subscriptions()
        result = await repo.upsert(subscription)
        await session.commit()
        logger.info("Seller subscriptions synced: tariff=%s", result.tariff)
        return result
