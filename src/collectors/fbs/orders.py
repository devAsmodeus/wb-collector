"""Коллектор: FBS — Сборочные задания."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.fbs.orders import (
    OrdersResponse, OrderStatusResponse, StickersResponse,
    OrderMetaResponse,
)


class OrdersCollector:
    def __init__(self):
        self._client = WBApiClient(
            base_url=settings.WB_MARKETPLACE_URL,
            token=settings.WB_API_TOKEN,
        )

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_new_orders(self) -> OrdersResponse:
        """GET /api/v3/orders/new — новые сборочные задания (ожидают сборки)."""
        data = await self._client.get("/api/v3/orders/new")
        return OrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def get_orders(
        self,
        date_from: int | None = None,
        date_to: int | None = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> OrdersResponse:
        """GET /api/v3/orders — сборочные задания за период."""
        params: dict = {"limit": limit, "offset": offset}
        if date_from: params["dateFrom"] = date_from
        if date_to: params["dateTo"] = date_to
        data = await self._client.get("/api/v3/orders", params=params)
        return OrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def get_orders_status(self, order_ids: list[int]) -> OrderStatusResponse:
        """POST /api/v3/orders/status — статусы сборочных заданий."""
        data = await self._client.post("/api/v3/orders/status", json={"orders": order_ids})
        return OrderStatusResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def get_reshipment_orders(self) -> OrdersResponse:
        """GET /api/v3/supplies/orders/reshipment — заказы для повторной отгрузки."""
        data = await self._client.get("/api/v3/supplies/orders/reshipment")
        return OrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def cancel_order(self, order_id: int) -> None:
        """PATCH /api/v3/orders/{orderId}/cancel — отменить сборочное задание."""
        await self._client.patch(f"/api/v3/orders/{order_id}/cancel")

    async def get_stickers(
        self,
        order_ids: list[int],
        sticker_type: str = "png",
        width: int = 58,
        height: int = 40,
    ) -> StickersResponse:
        """POST /api/v3/orders/stickers — стикеры для сборочных заданий."""
        params = {"type": sticker_type, "width": width, "height": height}
        data = await self._client.post("/api/v3/orders/stickers", json={"orders": order_ids}, params=params)
        return StickersResponse.model_validate(data if isinstance(data, dict) else {"stickers": data or []})

    async def get_orders_meta(self, order_ids: list[int]) -> OrderMetaResponse:
        """POST /api/marketplace/v3/orders/meta — метаданные сборочных заданий."""
        data = await self._client.post("/api/marketplace/v3/orders/meta", json={"orders": order_ids})
        return OrderMetaResponse.model_validate(data if isinstance(data, dict) else {"data": data})

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        """DELETE /api/v3/orders/{orderId}/meta — удалить метаданные задания."""
        await self._client.delete(f"/api/v3/orders/{order_id}/meta", params={"key": key})

    async def set_order_sgtin(self, order_id: int, sgtin: str) -> dict:
        """PUT /api/v3/orders/{orderId}/meta/sgtin — код маркировки (честный знак)."""
        return await self._client.put(f"/api/v3/orders/{order_id}/meta/sgtin", json={"sgtin": sgtin})

    async def set_order_uin(self, order_id: int, uin: str) -> dict:
        """PUT /api/v3/orders/{orderId}/meta/uin — УИН ювелирного изделия."""
        return await self._client.put(f"/api/v3/orders/{order_id}/meta/uin", json={"uin": uin})

    async def set_order_imei(self, order_id: int, imei: str) -> dict:
        """PUT /api/v3/orders/{orderId}/meta/imei — IMEI мобильного устройства."""
        return await self._client.put(f"/api/v3/orders/{order_id}/meta/imei", json={"imei": imei})

    async def set_order_gtin(self, order_id: int, gtin: str) -> dict:
        """PUT /api/v3/orders/{orderId}/meta/gtin — GTIN товара."""
        return await self._client.put(f"/api/v3/orders/{order_id}/meta/gtin", json={"gtin": gtin})

    async def set_order_expiration(self, order_id: int, expiration_date: str) -> dict:
        """PUT /api/v3/orders/{orderId}/meta/expiration — срок годности."""
        return await self._client.put(
            f"/api/v3/orders/{order_id}/meta/expiration",
            json={"expirationDate": expiration_date},
        )

    async def set_order_customs(self, order_id: int, customs_number: str) -> dict:
        """PUT /api/marketplace/v3/orders/{orderId}/meta/customs-declaration — номер ГТД."""
        return await self._client.put(
            f"/api/marketplace/v3/orders/{order_id}/meta/customs-declaration",
            json={"customsDeclarationNumber": customs_number},
        )

    async def get_crossborder_stickers(self, order_ids: list[int]) -> StickersResponse:
        """POST /api/v3/orders/stickers/cross-border — стикеры для кроссбордер заказов."""
        data = await self._client.post("/api/v3/orders/stickers/cross-border", json={"orders": order_ids})
        return StickersResponse.model_validate(data if isinstance(data, dict) else {"stickers": data or []})

    async def get_status_history(self, order_ids: list[int]) -> dict:
        """POST /api/v3/orders/status/history — история статусов кроссбордер заказов."""
        return await self._client.post("/api/v3/orders/status/history", json={"orders": order_ids})

    async def get_client_orders(self, order_ids: list[int]) -> dict:
        """POST /api/v3/orders/client — заказы с данными клиента."""
        return await self._client.post("/api/v3/orders/client", json={"orders": order_ids})
