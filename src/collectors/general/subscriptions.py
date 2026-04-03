"""Коллектор: Общее — Подписки Джем."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.general.subscriptions import SubscriptionsJamInfo


class SubscriptionsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_API_BASE_URL)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_subscriptions(self) -> SubscriptionsJamInfo:
        """GET /api/common/v1/subscriptions — подписки Джем."""
        data = await self._client.get("/api/common/v1/subscriptions")
        return SubscriptionsJamInfo.model_validate(data if isinstance(data, dict) else {})
