"""Сервис DB: Общее — Чтение подписок Джем из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.general.subscriptions import SubscriptionsRepository
from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.base import BaseService


class SubscriptionsDbService(BaseService):

    async def get_subscriptions(self, session: AsyncSession) -> SubscriptionsJamInfo | None:
        """Возвращает подписки Джем из таблицы wb_seller_subscriptions."""
        repo = SubscriptionsRepository(session)
        return await repo.get_one_or_none()
