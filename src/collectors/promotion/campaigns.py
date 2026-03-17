"""Коллектор: Маркетинг — Кампании."""
from src.collectors.base import WBApiClient
from src.config import settings


class CampaignsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_ADVERT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_count(self) -> dict:
        return await self._client.get("/adv/v1/promotion/count")

    async def get_adverts(self, ids: str | None = None, statuses: str | None = None, payment_type: str | None = None) -> dict:
        params: dict = {}
        if ids: params["ids"] = ids
        if statuses: params["statuses"] = statuses
        if payment_type: params["payment_type"] = payment_type
        return await self._client.get("/api/advert/v2/adverts", params=params)

    async def get_min_bids(self, payload: dict) -> dict:
        return await self._client.post("/api/advert/v1/bids/min", json=payload)

    async def create_campaign(self, payload: dict) -> dict:
        return await self._client.post("/adv/v2/seacat/save-ad", json=payload)

    async def get_subjects(self, payment_type: str | None = None) -> dict:
        params: dict = {}
        if payment_type: params["payment_type"] = payment_type
        return await self._client.get("/adv/v1/supplier/subjects", params=params)

    async def get_nms(self, nm_ids: list[int]) -> dict:
        return await self._client.post("/adv/v2/supplier/nms", json=nm_ids)

    async def delete_campaign(self, advert_id: int) -> dict:
        return await self._client.get("/adv/v0/delete", params={"id": advert_id})

    async def rename_campaign(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/rename", json=payload)

    async def start_campaign(self, advert_id: int) -> dict:
        return await self._client.get("/adv/v0/start", params={"id": advert_id})

    async def pause_campaign(self, advert_id: int) -> dict:
        return await self._client.get("/adv/v0/pause", params={"id": advert_id})

    async def stop_campaign(self, advert_id: int) -> dict:
        return await self._client.get("/adv/v0/stop", params={"id": advert_id})

    async def update_placements(self, payload: dict) -> dict:
        return await self._client.put("/adv/v0/auction/placements", json=payload)

    async def update_bids(self, payload: dict) -> dict:
        return await self._client.patch("/api/advert/v1/bids", json=payload)

    async def update_nms(self, payload: dict) -> dict:
        return await self._client.patch("/adv/v0/auction/nms", json=payload)

    async def get_bid_recommendations(self, nm_id: int | None = None, advert_id: int | None = None) -> dict:
        params: dict = {}
        if nm_id: params["nmId"] = nm_id
        if advert_id: params["advertId"] = advert_id
        return await self._client.get("/api/advert/v0/bids/recommendations", params=params)
