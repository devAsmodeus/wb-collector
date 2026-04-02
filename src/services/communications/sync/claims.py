"""Сервис Sync: Коммуникации — Синхронизация претензий."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.claims import ClaimsCollector
from src.repositories.communications.claims import ClaimsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class ClaimsSyncService(BaseService):

    async def sync_claims(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех претензий.
        Использует offset-based пагинацию.
        """
        repo = ClaimsRepository(session)
        all_claims: list[dict] = []

        async with ClaimsCollector() as collector:
            offset = 0
            limit = 100
            while True:
                response = await collector.get_claims(limit=limit, offset=offset, is_archive=False)
                claims = response.get("data", {}).get("claims", [])
                if not claims:
                    break
                all_claims.extend(claims)
                offset += limit

        saved = await repo.upsert_many(all_claims)
        logger.info(f"Claims synced: {saved} records saved")
        return {"synced": saved, "source": "full"}
