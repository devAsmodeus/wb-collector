"""Коллектор: Общее — АПИ новостей."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.general.news import NewsResponse


class NewsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_API_BASE_URL)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_news(
        self,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        """
        GET /api/communications/v2/news — новости портала продавцов.
        WB требует хотя бы один из параметров.
        По умолчанию — последние 90 дней.
        """
        params = {}
        if from_date:
            params["from"] = from_date
        if from_id is not None:
            params["fromID"] = from_id
        if not params:
            from datetime import datetime, timedelta
            params["from"] = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        data = await self._client.get("/api/communications/v2/news", params=params)
        return NewsResponse.model_validate(data)
