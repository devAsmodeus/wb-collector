"""Сервис WB: Коммуникации — Претензии."""
from src.collectors.communications.claims import ClaimsCollector
from src.schemas.communications.claims import UpdateClaimRequest
from src.services.base import BaseService


class ClaimsService(BaseService):
    async def get_claims(self, limit=10, offset=0) -> dict:
        async with ClaimsCollector() as c: return await c.get_claims(limit, offset)

    async def update_claim(self, data: UpdateClaimRequest) -> dict:
        async with ClaimsCollector() as c: return await c.update_claim(data.model_dump(exclude_none=True))
