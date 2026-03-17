"""Сервис: Маркетинг — Кампании."""
from src.collectors.promotion.campaigns import CampaignsCollector
from src.schemas.promotion.campaigns import (
    MinBidRequest, CreateCampaignRequest, RenameRequest,
    UpdatePlacementsRequest, UpdateBidsRequest, UpdateNmsRequest,
)
from src.services.base import BaseService


class CampaignsService(BaseService):
    async def get_count(self) -> dict:
        async with CampaignsCollector() as c: return await c.get_count()

    async def get_adverts(self, ids=None, statuses=None, payment_type=None) -> dict:
        async with CampaignsCollector() as c: return await c.get_adverts(ids, statuses, payment_type)

    async def get_min_bids(self, data: MinBidRequest) -> dict:
        async with CampaignsCollector() as c: return await c.get_min_bids(data.model_dump())

    async def create_campaign(self, data: CreateCampaignRequest) -> dict:
        async with CampaignsCollector() as c: return await c.create_campaign(data.model_dump())

    async def get_subjects(self, payment_type=None) -> dict:
        async with CampaignsCollector() as c: return await c.get_subjects(payment_type)

    async def get_nms(self, nm_ids: list[int]) -> dict:
        async with CampaignsCollector() as c: return await c.get_nms(nm_ids)

    async def delete_campaign(self, advert_id: int) -> dict:
        async with CampaignsCollector() as c: return await c.delete_campaign(advert_id)

    async def rename_campaign(self, data: RenameRequest) -> dict:
        async with CampaignsCollector() as c: return await c.rename_campaign(data.model_dump())

    async def start_campaign(self, advert_id: int) -> dict:
        async with CampaignsCollector() as c: return await c.start_campaign(advert_id)

    async def pause_campaign(self, advert_id: int) -> dict:
        async with CampaignsCollector() as c: return await c.pause_campaign(advert_id)

    async def stop_campaign(self, advert_id: int) -> dict:
        async with CampaignsCollector() as c: return await c.stop_campaign(advert_id)

    async def update_placements(self, data: UpdatePlacementsRequest) -> dict:
        async with CampaignsCollector() as c: return await c.update_placements(data.model_dump())

    async def update_bids(self, data: UpdateBidsRequest) -> dict:
        async with CampaignsCollector() as c: return await c.update_bids(data.model_dump())

    async def update_nms(self, data: UpdateNmsRequest) -> dict:
        async with CampaignsCollector() as c: return await c.update_nms(data.model_dump())

    async def get_bid_recommendations(self, nm_id=None, advert_id=None) -> dict:
        async with CampaignsCollector() as c: return await c.get_bid_recommendations(nm_id, advert_id)
