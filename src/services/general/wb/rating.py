"""Сервис WB: Общее — Рейтинг продавца."""
from src.collectors.general.rating import RatingCollector
from src.schemas.general.rating import SupplierRatingModel
from src.services.base import BaseService


class RatingWbService(BaseService):

    async def get_rating(self) -> SupplierRatingModel:
        """Получает рейтинг продавца из WB API (без сохранения в БД)."""
        async with RatingCollector() as c:
            return await c.get_rating()
