"""Коллектор: DBS — Сборочные задания."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.dbs.orders import DBSOrdersResponse, DBSOrderStatusResponse, DBSStickersResponse


class DBSOrdersCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_MARKETPLACE_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_new_orders(self) -> DBSOrdersResponse:
        data = await self._client.get("/api/v3/dbs/orders/new")
        return DBSOrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def get_orders(self, date_from=None, date_to=None) -> DBSOrdersResponse:
        params: dict = {}
        if date_from: params["dateFrom"] = date_from
        if date_to: params["dateTo"] = date_to
        data = await self._client.get("/api/v3/dbs/orders", params=params)
        return DBSOrdersResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def get_group_info(self, order_ids: list[int]) -> dict:
        return await self._client.post("/api/v3/dbs/groups/info", json={"orders": order_ids})

    async def get_client_orders(self, order_ids: list[int]) -> dict:
        return await self._client.post("/api/v3/dbs/orders/client", json={"orders": order_ids})

    async def get_b2b_info(self, order_ids: list[int]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/b2b/info", json={"orders": order_ids})

    async def set_delivery_date(self, order_ids: list[int], delivery_date: str) -> None:
        await self._client.post("/api/v3/dbs/orders/delivery-date", json={"orders": order_ids, "deliveryDate": delivery_date})

    async def get_orders_status(self, order_ids: list[int]) -> DBSOrderStatusResponse:
        data = await self._client.post("/api/marketplace/v3/dbs/orders/status/info", json={"orders": order_ids})
        return DBSOrderStatusResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def cancel_orders(self, order_ids: list[int]) -> None:
        await self._client.post("/api/marketplace/v3/dbs/orders/status/cancel", json={"orders": order_ids})

    async def confirm_orders(self, order_ids: list[int]) -> None:
        await self._client.post("/api/marketplace/v3/dbs/orders/status/confirm", json={"orders": order_ids})

    async def get_stickers(self, order_ids: list[int], sticker_type="png", width=58, height=40) -> DBSStickersResponse:
        params = {"type": sticker_type, "width": width, "height": height}
        data = await self._client.post("/api/marketplace/v3/dbs/orders/stickers", json={"orders": order_ids}, params=params)
        return DBSStickersResponse.model_validate(data if isinstance(data, dict) else {"stickers": data or []})

    async def deliver_orders(self, order_ids: list[int]) -> None:
        await self._client.post("/api/marketplace/v3/dbs/orders/status/deliver", json={"orders": order_ids})

    async def receive_orders(self, order_ids: list[int]) -> None:
        await self._client.post("/api/marketplace/v3/dbs/orders/status/receive", json={"orders": order_ids})

    async def reject_orders(self, order_ids: list[int], reason: str | None = None) -> None:
        body: dict = {"orders": order_ids}
        if reason: body["reason"] = reason
        await self._client.post("/api/marketplace/v3/dbs/orders/status/reject", json=body)

    # --- Deprecated ---
    async def get_orders_status_deprecated(self, order_ids: list[int]) -> DBSOrderStatusResponse:
        data = await self._client.post("/api/v3/dbs/orders/status", json={"orders": order_ids})
        return DBSOrderStatusResponse.model_validate(data if isinstance(data, dict) else {"orders": data or []})

    async def cancel_order(self, order_id: int) -> None:
        await self._client.patch(f"/api/v3/dbs/orders/{order_id}/cancel")

    async def confirm_order(self, order_id: int) -> None:
        await self._client.patch(f"/api/v3/dbs/orders/{order_id}/confirm")

    async def deliver_order(self, order_id: int) -> None:
        await self._client.patch(f"/api/v3/dbs/orders/{order_id}/deliver")

    async def receive_order(self, order_id: int, payload: dict) -> None:
        await self._client.patch(f"/api/v3/dbs/orders/{order_id}/receive", json=payload)

    async def reject_order(self, order_id: int, payload: dict) -> None:
        await self._client.patch(f"/api/v3/dbs/orders/{order_id}/reject", json=payload)
