"""Коллектор: DBW — Сборочные задания."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.dbw.orders import (
    DBWOrdersResponse, DBWOrderStatusResponse, DBWStickersResponse,
)


class DBWOrdersCollector:
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

    async def get_new_orders(self) -> DBWOrdersResponse:
        """GET /api/v3/dbw/orders/new — новые сборочные задания DBW."""
        data = await self._client.get("/api/v3/dbw/orders/new")
        return DBWOrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def get_orders(self, date_from: int | None = None, date_to: int | None = None) -> DBWOrdersResponse:
        """GET /api/v3/dbw/orders — задания за период."""
        params: dict = {}
        if date_from: params["dateFrom"] = date_from
        if date_to: params["dateTo"] = date_to
        data = await self._client.get("/api/v3/dbw/orders", params=params)
        return DBWOrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def set_delivery_date(self, order_ids: list[int], delivery_date: str) -> None:
        """POST /api/v3/dbw/orders/delivery-date — установить дату доставки."""
        await self._client.post(
            "/api/v3/dbw/orders/delivery-date",
            json={"orders": order_ids, "deliveryDate": delivery_date},
        )

    async def get_client_orders(self, order_ids: list[int]) -> dict:
        """POST /api/marketplace/v3/dbw/orders/client — заказы с данными клиента."""
        return await self._client.post("/api/marketplace/v3/dbw/orders/client", json={"orders": order_ids})

    async def get_orders_status(self, order_ids: list[int]) -> DBWOrderStatusResponse:
        """POST /api/v3/dbw/orders/status — статусы заданий."""
        data = await self._client.post("/api/v3/dbw/orders/status", json={"orders": order_ids})
        return DBWOrderStatusResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def confirm_order(self, order_id: int) -> None:
        """PATCH /api/v3/dbw/orders/{orderId}/confirm — подтвердить задание."""
        await self._client.patch(f"/api/v3/dbw/orders/{order_id}/confirm")

    async def get_stickers(self, order_ids: list[int], sticker_type: str = "png", width: int = 58, height: int = 40) -> DBWStickersResponse:
        """POST /api/v3/dbw/orders/stickers — стикеры для заданий."""
        params = {"type": sticker_type, "width": width, "height": height}
        data = await self._client.post("/api/v3/dbw/orders/stickers", json={"orders": order_ids}, params=params)
        return DBWStickersResponse.model_validate(data if isinstance(data, dict) else {"stickers": data or []})

    async def assemble_order(self, order_id: int) -> None:
        """PATCH /api/v3/dbw/orders/{orderId}/assemble — отметить задание как собранное."""
        await self._client.patch(f"/api/v3/dbw/orders/{order_id}/assemble")

    async def call_courier(self, order_ids: list[int]) -> None:
        """POST /api/v3/dbw/orders/courier — вызвать курьера WB."""
        await self._client.post("/api/v3/dbw/orders/courier", json={"orders": order_ids})

    async def cancel_order(self, order_id: int) -> None:
        """PATCH /api/v3/dbw/orders/{orderId}/cancel — отменить задание."""
        await self._client.patch(f"/api/v3/dbw/orders/{order_id}/cancel")
