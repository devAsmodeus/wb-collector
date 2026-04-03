"""DB: Общее — Подписки Джем."""
from litestar import Controller, get

from src.repositories.general.subscriptions import SubscriptionsRepository
from src.utils.db_manager import DBManager


class DbSubscriptionsController(Controller):
    path = "/subscriptions"
    tags = ["01. База данных"]

    @get(summary="Подписки Джем из БД")
    async def get_subscriptions(self) -> dict:
        async with DBManager() as db:
            repo = SubscriptionsRepository(db.session)
            subs = await repo.get_one_or_none()
            data = [subs.model_dump()] if subs else []
            return {"data": data, "total": len(data), "limit": 1, "offset": 0}
