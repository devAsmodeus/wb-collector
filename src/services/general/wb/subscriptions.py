"""Сервис WB: Общее — Подписки Джем."""
from src.collectors.general.subscriptions import SubscriptionsCollector
from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.base import BaseService


class SubscriptionsWbService(BaseService):

    async def get_subscriptions(self) -> SubscriptionsJamInfo:
        """Получает подписки Джем из WB API (без сохранения в БД)."""
        async with SubscriptionsCollector() as c:
            return await c.get_subscriptions()
