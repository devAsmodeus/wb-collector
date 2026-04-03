"""Коллектор: Общее — Рейтинг продавца."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.general.rating import SupplierRatingModel


class RatingCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FEEDBACKS_URL)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_rating(self) -> SupplierRatingModel:
        """GET /api/common/v1/rating — рейтинг продавца."""
        data = await self._client.get("/api/common/v1/rating")
        return SupplierRatingModel.model_validate(data if isinstance(data, dict) else {})
