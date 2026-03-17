"""Коллектор: DBW — Метаданные сборочных заданий."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.dbw.meta import DBWOrderMetaResponse


class DBWMetaCollector:
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

    async def get_order_meta(self, order_id: int) -> DBWOrderMetaResponse:
        """GET /api/v3/dbw/orders/{orderId}/meta — метаданные задания."""
        data = await self._client.get(f"/api/v3/dbw/orders/{order_id}/meta")
        return DBWOrderMetaResponse.model_validate(data if isinstance(data, dict) else {"meta": data})

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        """DELETE /api/v3/dbw/orders/{orderId}/meta — удалить метаданные."""
        await self._client.delete(f"/api/v3/dbw/orders/{order_id}/meta", params={"key": key})

    async def set_sgtin(self, order_id: int, sgtins: list[str]) -> dict:
        """PUT /api/v3/dbw/orders/{orderId}/meta/sgtin — коды маркировки."""
        return await self._client.put(f"/api/v3/dbw/orders/{order_id}/meta/sgtin", json={"sgtins": sgtins})

    async def set_uin(self, order_id: int, uin: str) -> dict:
        """PUT /api/v3/dbw/orders/{orderId}/meta/uin — УИН ювелирного изделия."""
        return await self._client.put(f"/api/v3/dbw/orders/{order_id}/meta/uin", json={"uin": uin})

    async def set_imei(self, order_id: int, imei: str) -> dict:
        """PUT /api/v3/dbw/orders/{orderId}/meta/imei — IMEI устройства."""
        return await self._client.put(f"/api/v3/dbw/orders/{order_id}/meta/imei", json={"imei": imei})

    async def set_gtin(self, order_id: int, gtin: str) -> dict:
        """PUT /api/v3/dbw/orders/{orderId}/meta/gtin — GTIN товара."""
        return await self._client.put(f"/api/v3/dbw/orders/{order_id}/meta/gtin", json={"gtin": gtin})
