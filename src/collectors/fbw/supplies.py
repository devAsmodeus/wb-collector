"""Коллектор: FBW — Информация о поставках."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.fbw.supplies import FBWSuppliesResponse, FBWSupplyGoodsResponse, FBWPackageQR


class FBWSuppliesCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_MARKETPLACE_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_supplies(
        self,
        payload: dict,
        limit: int = 1000,
        offset: int = 0,
    ) -> FBWSuppliesResponse:
        """POST /api/v1/supplies — список поставок с фильтрами."""
        data = await self._client.post(
            "/api/v1/supplies",
            json=payload,
            params={"limit": limit, "offset": offset},
        )
        return FBWSuppliesResponse.model_validate(
            data if isinstance(data, dict) else {"supplies": data or []}
        )

    async def get_supply(self, supply_id: int, is_preorder_id: bool = False) -> dict:
        """GET /api/v1/supplies/{ID} — детали поставки."""
        return await self._client.get(
            f"/api/v1/supplies/{supply_id}",
            params={"isPreorderID": is_preorder_id},
        )

    async def get_supply_goods(
        self,
        supply_id: int,
        limit: int = 1000,
        offset: int = 0,
        is_preorder_id: bool = False,
    ) -> FBWSupplyGoodsResponse:
        """GET /api/v1/supplies/{ID}/goods — товары поставки."""
        data = await self._client.get(
            f"/api/v1/supplies/{supply_id}/goods",
            params={"limit": limit, "offset": offset, "isPreorderID": is_preorder_id},
        )
        return FBWSupplyGoodsResponse.model_validate(
            data if isinstance(data, dict) else {"goods": data or []}
        )

    async def get_supply_package(self, supply_id: int) -> FBWPackageQR:
        """GET /api/v1/supplies/{ID}/package — QR-код упаковки поставки."""
        data = await self._client.get(f"/api/v1/supplies/{supply_id}/package")
        return FBWPackageQR.model_validate(data if isinstance(data, dict) else {"file": data})
