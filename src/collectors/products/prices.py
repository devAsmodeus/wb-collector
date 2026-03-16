"""Коллектор: Работа с товарами — Цены и скидки (11 методов).
Хост: discounts-prices-api.wildberries.ru
✅ Работает с текущим токеном (скоуп: Цены и скидки, bit 4).
"""
from src.collectors.base import WBApiClient
from src.schemas.products.prices import GoodsListResponse


class PricesCollector:
    def __init__(self, client: WBApiClient):
        self._client = client

    async def get_goods_list(self, limit: int = 100, offset: int = 0, filter_nm_id: int | None = None) -> GoodsListResponse:
        """GET /api/v2/list/goods/filter — товары с ценами и скидками."""
        params = {"limit": limit, "offset": offset}
        if filter_nm_id is not None:
            params["filterNmID"] = filter_nm_id
        data = await self._client.get("/api/v2/list/goods/filter", params=params)
        return GoodsListResponse.model_validate(data)

    async def get_goods_list_by_nm(self, nm_ids: list[int]) -> GoodsListResponse:
        """POST /api/v2/list/goods/filter — товары по списку артикулов."""
        data = await self._client.post("/api/v2/list/goods/filter", json={"nmIDs": nm_ids})
        return GoodsListResponse.model_validate(data)

    async def get_goods_sizes(self, nm_id: int) -> dict:
        """GET /api/v2/list/goods/size/nm — цены по размерам артикула."""
        return await self._client.get("/api/v2/list/goods/size/nm", params={"nmId": nm_id})

    async def get_quarantine_goods(self, limit: int = 100, offset: int = 0) -> dict:
        """GET /api/v2/quarantine/goods — товары на карантине."""
        return await self._client.get(
            "/api/v2/quarantine/goods", params={"limit": limit, "offset": offset}
        )

    async def set_prices_and_discounts(self, tasks: list[dict]) -> dict:
        """
        POST /api/v2/upload/task — установить цены и скидки.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/api/v2/upload/task", json={"data": tasks})

    async def set_prices_for_sizes(self, tasks: list[dict]) -> dict:
        """
        POST /api/v2/upload/task/size — установить цены для размеров.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/api/v2/upload/task/size", json={"data": tasks})

    async def set_club_discounts(self, tasks: list[dict]) -> dict:
        """
        POST /api/v2/upload/task/club-discount — скидки WB Клуба.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        return await self._client.post("/api/v2/upload/task/club-discount", json={"data": tasks})

    async def get_price_upload_history(self, limit: int = 100, offset: int = 0) -> dict:
        """GET /api/v2/history/tasks — история загрузок цен."""
        return await self._client.get(
            "/api/v2/history/tasks", params={"limit": limit, "offset": offset}
        )

    async def get_price_upload_goods(self, upload_id: int) -> dict:
        """GET /api/v2/history/goods/task — товары конкретной загрузки."""
        return await self._client.get(
            "/api/v2/history/goods/task", params={"uploadID": upload_id}
        )

    async def get_buffer_tasks(self, limit: int = 100, offset: int = 0) -> dict:
        """GET /api/v2/buffer/tasks — задачи в буфере цен."""
        return await self._client.get(
            "/api/v2/buffer/tasks", params={"limit": limit, "offset": offset}
        )

    async def get_buffer_goods(self, upload_id: int) -> dict:
        """GET /api/v2/buffer/goods/task — товары задачи в буфере."""
        return await self._client.get(
            "/api/v2/buffer/goods/task", params={"uploadID": upload_id}
        )
