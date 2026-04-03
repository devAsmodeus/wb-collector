"""Сервис DB: Общее — Чтение рейтинга продавца из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.general.rating import RatingRepository
from src.schemas.general.rating import SupplierRatingModel
from src.services.base import BaseService


class RatingDbService(BaseService):

    async def get_rating(self, session: AsyncSession) -> SupplierRatingModel | None:
        """Возвращает рейтинг продавца из таблицы wb_seller_rating."""
        repo = RatingRepository(session)
        return await repo.get_one_or_none()
