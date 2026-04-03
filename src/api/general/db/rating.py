"""DB: Общее — Рейтинг продавца."""
from litestar import Controller, get

from src.repositories.general.rating import RatingRepository
from src.utils.db_manager import DBManager


class DbRatingController(Controller):
    path = "/rating"
    tags = ["01. База данных"]

    @get(summary="Рейтинг продавца из БД")
    async def get_rating(self) -> dict:
        async with DBManager() as db:
            repo = RatingRepository(db.session)
            rating = await repo.get_one_or_none()
            data = [rating.model_dump()] if rating else []
            return {"data": data, "total": len(data), "limit": 1, "offset": 0}
