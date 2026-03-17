"""Коллектор: Финансы WB."""
from src.collectors.base import WBApiClient
from src.config import settings


class FinancesCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FINANCES_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_balance(self) -> dict:
        return await self._client.get("/api/v1/account/balance")

    async def get_financial_report(
        self,
        date_from: str,
        date_to: str,
        limit: int = 100000,
        rrdid: int = 0,
        period: int | None = None,
    ) -> list:
        params: dict = {"dateFrom": date_from, "dateTo": date_to, "limit": limit, "rrdid": rrdid}
        if period is not None:
            params["period"] = period
        return await self._client.get("/api/v5/supplier/reportDetailByPeriod", params=params)

    async def get_document_categories(self) -> dict:
        return await self._client.get("/api/v1/documents/categories")

    async def get_documents(
        self,
        begin_time: str | None = None,
        end_time: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        category: str | None = None,
        service_name: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        params: dict = {"limit": limit, "offset": offset}
        if begin_time: params["beginTime"] = begin_time
        if end_time: params["endTime"] = end_time
        if sort: params["sort"] = sort
        if order: params["order"] = order
        if category: params["category"] = category
        if service_name: params["serviceName"] = service_name
        return await self._client.get("/api/v1/documents/list", params=params)

    async def download_document(self, service_name: str, extension: str) -> dict:
        return await self._client.get(
            "/api/v1/documents/download",
            params={"serviceName": service_name, "extension": extension},
        )

    async def download_all_documents(self, payload: dict) -> dict:
        return await self._client.post("/api/v1/documents/download/all", json=payload)
