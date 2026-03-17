"""Коллектор: DBS — Метаданные сборочных заданий."""
from src.collectors.base import WBApiClient
from src.config import settings


class DBSMetaCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_MARKETPLACE_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_meta_info(self, order_ids: list[int]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/meta/info", json={"orders": order_ids})

    async def delete_meta(self, order_ids: list[int], key: str) -> None:
        await self._client.post("/api/marketplace/v3/dbs/orders/meta/delete", json={"orders": order_ids, "key": key})

    async def set_sgtin(self, orders: list[dict]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/meta/sgtin", json={"orders": orders})

    async def set_uin(self, orders: list[dict]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/meta/uin", json={"orders": orders})

    async def set_imei(self, orders: list[dict]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/meta/imei", json={"orders": orders})

    async def set_gtin(self, orders: list[dict]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/meta/gtin", json={"orders": orders})

    async def set_customs(self, orders: list[dict]) -> dict:
        return await self._client.post("/api/marketplace/v3/dbs/orders/meta/customs-declaration", json={"orders": orders})

    # --- Deprecated ---
    async def get_order_meta(self, order_id: int) -> dict:
        return await self._client.get(f"/api/v3/dbs/orders/{order_id}/meta")

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        await self._client.delete(f"/api/v3/dbs/orders/{order_id}/meta", params={"key": key})

    async def set_sgtin_single(self, order_id: int, sgtins: list[str]) -> dict:
        return await self._client.put(f"/api/v3/dbs/orders/{order_id}/meta/sgtin", json={"sgtins": sgtins})

    async def set_uin_single(self, order_id: int, uin: str) -> dict:
        return await self._client.put(f"/api/v3/dbs/orders/{order_id}/meta/uin", json={"uin": uin})

    async def set_imei_single(self, order_id: int, imei: str) -> dict:
        return await self._client.put(f"/api/v3/dbs/orders/{order_id}/meta/imei", json={"imei": imei})

    async def set_gtin_single(self, order_id: int, gtin: str) -> dict:
        return await self._client.put(f"/api/v3/dbs/orders/{order_id}/meta/gtin", json={"gtin": gtin})
