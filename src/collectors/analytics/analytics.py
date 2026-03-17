"""Коллектор: Аналитика WB."""
from src.collectors.base import WBApiClient
from src.config import settings


class AnalyticsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_ANALYTICS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    # Воронка продаж
    async def get_funnel_products(self, payload: dict) -> dict:
        return await self._client.post("/api/analytics/v3/sales-funnel/products", json=payload)

    async def get_funnel_products_history(self, payload: dict) -> dict:
        return await self._client.post("/api/analytics/v3/sales-funnel/products/history", json=payload)

    async def get_funnel_grouped_history(self, payload: dict) -> dict:
        return await self._client.post("/api/analytics/v3/sales-funnel/grouped/history", json=payload)

    # CSV-отчёты
    async def create_nm_report(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/nm-report/downloads", json=payload)

    async def get_nm_reports(self, download_ids: str | None = None) -> dict:
        params = {}
        if download_ids:
            params["filter[downloadIds]"] = download_ids
        return await self._client.get("/api/v2/nm-report/downloads", params=params)

    async def retry_nm_report(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/nm-report/downloads/retry", json=payload)

    async def get_nm_report_file(self, download_id: str) -> dict:
        return await self._client.get(f"/api/v2/nm-report/downloads/file/{download_id}")

    # Поисковые запросы
    async def get_search_report(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/search-report/report", json=payload)

    async def get_search_groups(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/search-report/table/groups", json=payload)

    async def get_search_details(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/search-report/table/details", json=payload)

    async def get_search_texts(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/search-report/product/search-texts", json=payload)

    async def get_search_orders(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/search-report/product/orders", json=payload)

    # История остатков
    async def get_stocks_groups(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/stocks-report/products/groups", json=payload)

    async def get_stocks_products(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/stocks-report/products/products", json=payload)

    async def get_stocks_sizes(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/stocks-report/products/sizes", json=payload)

    async def get_stocks_offices(self, payload: dict) -> dict:
        return await self._client.post("/api/v2/stocks-report/offices", json=payload)
