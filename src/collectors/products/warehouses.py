"""Коллектор: Работа с товарами — Остатки и склады продавца (10 методов).
Хосты:
  marketplace-api.wildberries.ru — /api/v3/stocks/*, /api/v3/warehouses/*
✅ Работает с текущим токеном (скоуп: Маркетплейс FBS, bit 8).
"""
from src.collectors.base import WBApiClient
from src.schemas.products.warehouses import (
    WBOfficesResponse, SellerWarehousesResponse, DBWContactsResponse,
)


class WarehousesCollector:
    def __init__(self, client: WBApiClient):
        self._client = client

    async def get_wb_offices(self) -> WBOfficesResponse:
        """GET /api/v3/offices — список офисов WB (пункты сдачи)."""
        data = await self._client.get("/api/v3/offices")
        if isinstance(data, list):
            return WBOfficesResponse(result=data)
        return WBOfficesResponse.model_validate(data)

    async def get_seller_warehouses(self) -> SellerWarehousesResponse:
        """GET /api/v3/warehouses — склады продавца."""
        data = await self._client.get("/api/v3/warehouses")
        if isinstance(data, list):
            return SellerWarehousesResponse(result=data)
        return SellerWarehousesResponse.model_validate(data)

    async def create_seller_warehouse(self, name: str, office_id: int) -> dict:
        """
        POST /api/v3/warehouses — создать склад продавца.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post(
            "/api/v3/warehouses", json={"name": name, "officeId": office_id}
        )

    async def update_seller_warehouse(self, warehouse_id: int, name: str, office_id: int) -> dict:
        """
        PUT /api/v3/warehouses/{warehouseId} — обновить склад продавца.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.put(
            f"/api/v3/warehouses/{warehouse_id}",
            json={"name": name, "officeId": office_id},
        )

    async def delete_seller_warehouse(self, warehouse_id: int) -> dict:
        """
        DELETE /api/v3/warehouses/{warehouseId} — удалить склад продавца.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.delete(f"/api/v3/warehouses/{warehouse_id}")

    async def get_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        """POST /api/v3/stocks/{warehouseId} — остатки товаров на складе."""
        return await self._client.post(
            f"/api/v3/stocks/{warehouse_id}", json={"skus": skus}
        )

    async def update_stocks(self, warehouse_id: int, stocks: list[dict]) -> dict:
        """
        PUT /api/v3/stocks/{warehouseId} — обновить остатки.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        Формат: [{"sku": "...", "amount": N}]
        """
        return await self._client.put(
            f"/api/v3/stocks/{warehouse_id}", json={"stocks": stocks}
        )

    async def delete_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        """
        DELETE /api/v3/stocks/{warehouseId} — обнулить остатки.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.delete(
            f"/api/v3/stocks/{warehouse_id}", json={"skus": skus}
        )

    async def get_dbw_contacts(self, warehouse_id: int) -> DBWContactsResponse:
        """GET /api/v3/dbw/warehouses/{warehouseId}/contacts — контакты склада DBW."""
        data = await self._client.get(f"/api/v3/dbw/warehouses/{warehouse_id}/contacts")
        return DBWContactsResponse.model_validate(data)

    async def update_dbw_contacts(self, warehouse_id: int, contacts: list[dict]) -> dict:
        """
        PUT /api/v3/dbw/warehouses/{warehouseId}/contacts — обновить контакты DBW.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.put(
            f"/api/v3/dbw/warehouses/{warehouse_id}/contacts",
            json={"contacts": contacts},
        )
