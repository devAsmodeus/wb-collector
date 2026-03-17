"""Коллектор: Отчёты WB."""
from src.collectors.base import WBApiClient
from src.config import settings


class ReportsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_STATS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    # Основные отчёты
    async def get_stocks(self, date_from: str) -> list:
        return await self._client.get("/api/v1/supplier/stocks", params={"dateFrom": date_from})

    async def get_orders(self, date_from: str) -> list:
        return await self._client.get("/api/v1/supplier/orders", params={"dateFrom": date_from})

    async def get_sales(self, date_from: str) -> list:
        return await self._client.get("/api/v1/supplier/sales", params={"dateFrom": date_from})

    async def get_excise_report(self, payload: dict) -> dict:
        return await self._client.post("/api/v1/analytics/excise-report", json=payload)

    # Остатки на складах (async task)
    async def create_warehouse_remains_task(self, params: dict) -> dict:
        return await self._client.get("/api/v1/warehouse_remains", params=params)

    async def get_warehouse_remains_status(self, task_id: str) -> dict:
        return await self._client.get(f"/api/v1/warehouse_remains/tasks/{task_id}/status")

    async def download_warehouse_remains(self, task_id: str) -> dict:
        return await self._client.get(f"/api/v1/warehouse_remains/tasks/{task_id}/download")

    # Удержания
    async def get_measurement_penalties(self, date_from: str, date_to: str, limit: int = 100, offset: int = 0) -> dict:
        return await self._client.get(
            "/api/analytics/v1/measurement-penalties",
            params={"dateFrom": date_from, "dateTo": date_to, "limit": limit, "offset": offset},
        )

    async def get_warehouse_measurements(self, date_from: str, date_to: str, limit: int = 100, offset: int = 0) -> dict:
        return await self._client.get(
            "/api/analytics/v1/warehouse-measurements",
            params={"dateFrom": date_from, "dateTo": date_to, "limit": limit, "offset": offset},
        )

    async def get_deductions(self, date_from: str, date_to: str, sort: str | None = None, order: str | None = None, limit: int = 100, offset: int = 0) -> dict:
        params: dict = {"dateFrom": date_from, "dateTo": date_to, "limit": limit, "offset": offset}
        if sort: params["sort"] = sort
        if order: params["order"] = order
        return await self._client.get("/api/analytics/v1/deductions", params=params)

    async def get_antifraud_details(self) -> dict:
        return await self._client.get("/api/v1/analytics/antifraud-details")

    async def get_goods_labeling(self) -> dict:
        return await self._client.get("/api/v1/analytics/goods-labeling")

    # Приёмка (async task)
    async def create_acceptance_report_task(self) -> dict:
        return await self._client.get("/api/v1/acceptance_report")

    async def get_acceptance_report_status(self, task_id: str) -> dict:
        return await self._client.get(f"/api/v1/acceptance_report/tasks/{task_id}/status")

    async def download_acceptance_report(self, task_id: str) -> dict:
        return await self._client.get(f"/api/v1/acceptance_report/tasks/{task_id}/download")

    # Платное хранение (async task)
    async def create_paid_storage_task(self, date_from: str, date_to: str) -> dict:
        return await self._client.get("/api/v1/paid_storage", params={"dateFrom": date_from, "dateTo": date_to})

    async def get_paid_storage_status(self, task_id: str) -> dict:
        return await self._client.get(f"/api/v1/paid_storage/tasks/{task_id}/status")

    async def download_paid_storage(self, task_id: str) -> dict:
        return await self._client.get(f"/api/v1/paid_storage/tasks/{task_id}/download")

    # Региональные продажи
    async def get_region_sale(self) -> dict:
        return await self._client.get("/api/v1/analytics/region-sale")

    # Доля бренда
    async def get_brand_brands(self) -> dict:
        return await self._client.get("/api/v1/analytics/brand-share/brands")

    async def get_brand_parent_subjects(self, locale: str | None = None, brand: str | None = None) -> dict:
        params: dict = {}
        if locale: params["locale"] = locale
        if brand: params["brand"] = brand
        return await self._client.get("/api/v1/analytics/brand-share/parent-subjects", params=params)

    async def get_brand_share(self, parent_id: int, brand: str) -> dict:
        return await self._client.get("/api/v1/analytics/brand-share", params={"parentId": parent_id, "brand": brand})

    # Скрытые товары
    async def get_blocked_products(self, sort: str | None = None, order: str | None = None) -> dict:
        params: dict = {}
        if sort: params["sort"] = sort
        if order: params["order"] = order
        return await self._client.get("/api/v1/analytics/banned-products/blocked", params=params)

    async def get_shadowed_products(self, sort: str | None = None, order: str | None = None) -> dict:
        params: dict = {}
        if sort: params["sort"] = sort
        if order: params["order"] = order
        return await self._client.get("/api/v1/analytics/banned-products/shadowed", params=params)

    # Возвраты
    async def get_goods_return(self, date_from: str, date_to: str) -> dict:
        return await self._client.get("/api/v1/analytics/goods-return", params={"dateFrom": date_from, "dateTo": date_to})
