"""Сервис Sync: Общее — Синхронизация рейтинга продавца."""
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.general.rating import RatingCollector
from src.repositories.general.rating import RatingRepository
from src.schemas.general.rating import SupplierRatingModel
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class RatingSyncService(BaseService):

    async def sync_full(self, session: AsyncSession) -> SupplierRatingModel:
        """Запрашивает рейтинг у WB и сохраняет/обновляет в таблице wb_seller_rating."""
        repo = RatingRepository(session)
        async with RatingCollector() as c:
            rating = await c.get_rating()
        result = await repo.upsert(rating)
        await session.commit()
        logger.info("Seller rating synced: current=%s", result.current)
        return result
