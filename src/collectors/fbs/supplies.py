"""Коллектор: FBS — Поставки и короба."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.fbs.supplies import (
    SuppliesResponse, CreateSupplyResponse,
    SupplyOrdersResponse, SupplyOrderIdsResponse,
    SupplyBarcode, BoxesResponse, BoxStickersResponse,
)


class SuppliesCollector:
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

    async def create_supply(self, name: str) -> CreateSupplyResponse:
        """POST /api/v3/supplies — создать новую поставку."""
        data = await self._client.post("/api/v3/supplies", json={"name": name})
        return CreateSupplyResponse.model_validate(data)

    async def get_supplies(self, limit: int = 1000, offset: int = 0) -> SuppliesResponse:
        """GET /api/v3/supplies — список поставок."""
        data = await self._client.get("/api/v3/supplies", params={"limit": limit, "next": offset})
        return SuppliesResponse.model_validate(data if isinstance(data, dict) else {"supplies": data or []})

    async def get_supply(self, supply_id: str) -> dict:
        """GET /api/v3/supplies/{supplyId} — информация о поставке."""
        return await self._client.get(f"/api/v3/supplies/{supply_id}")

    async def delete_supply(self, supply_id: str) -> None:
        """DELETE /api/v3/supplies/{supplyId} — удалить поставку."""
        await self._client.delete(f"/api/v3/supplies/{supply_id}")

    async def add_orders_to_supply(self, supply_id: str, order_ids: list[int]) -> None:
        """PATCH /api/marketplace/v3/supplies/{supplyId}/orders — добавить заказы в поставку."""
        await self._client.patch(
            f"/api/marketplace/v3/supplies/{supply_id}/orders",
            json={"orders": order_ids},
        )

    async def get_supply_order_ids(self, supply_id: str) -> SupplyOrderIdsResponse:
        """GET /api/marketplace/v3/supplies/{supplyId}/order-ids — ID заказов поставки."""
        data = await self._client.get(f"/api/marketplace/v3/supplies/{supply_id}/order-ids")
        return SupplyOrderIdsResponse.model_validate(data if isinstance(data, dict) else {"orderIds": data or []})

    async def deliver_supply(self, supply_id: str) -> None:
        """PATCH /api/v3/supplies/{supplyId}/deliver — передать поставку в доставку."""
        await self._client.patch(f"/api/v3/supplies/{supply_id}/deliver")

    async def get_supply_barcode(self, supply_id: str, barcode_type: str = "svg") -> SupplyBarcode:
        """GET /api/v3/supplies/{supplyId}/barcode — QR-код поставки."""
        data = await self._client.get(
            f"/api/v3/supplies/{supply_id}/barcode",
            params={"type": barcode_type},
        )
        return SupplyBarcode.model_validate(data if isinstance(data, dict) else {"file": data})

    async def get_supply_boxes(self, supply_id: str) -> BoxesResponse:
        """GET /api/v3/supplies/{supplyId}/trbx — список коробов поставки."""
        data = await self._client.get(f"/api/v3/supplies/{supply_id}/trbx")
        return BoxesResponse.model_validate(data if isinstance(data, dict) else {"trbx": data or []})

    async def add_boxes(self, supply_id: str, quantity: int) -> BoxesResponse:
        """POST /api/v3/supplies/{supplyId}/trbx — добавить короба к поставке."""
        data = await self._client.post(f"/api/v3/supplies/{supply_id}/trbx", json={"quantity": quantity})
        return BoxesResponse.model_validate(data if isinstance(data, dict) else {"trbx": data or []})

    async def delete_boxes(self, supply_id: str, box_ids: list[str]) -> None:
        """DELETE /api/v3/supplies/{supplyId}/trbx — удалить короба из поставки."""
        await self._client.delete(f"/api/v3/supplies/{supply_id}/trbx", json={"trbx": box_ids})

    async def get_box_stickers(
        self,
        supply_id: str,
        box_ids: list[str],
        sticker_type: str = "png",
    ) -> BoxStickersResponse:
        """POST /api/v3/supplies/{supplyId}/trbx/stickers — стикеры для коробов."""
        data = await self._client.post(
            f"/api/v3/supplies/{supply_id}/trbx/stickers",
            json={"trbx": box_ids},
            params={"type": sticker_type},
        )
        return BoxStickersResponse.model_validate(data if isinstance(data, dict) else {"stickers": data or []})
