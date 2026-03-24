"""Сервис DB: Коммуникации — Чтение претензий из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.communications.claims import ClaimsRepository
from src.services.base import BaseService


class ClaimsDbService(BaseService):

    async def get_claims(
        self,
        session: AsyncSession,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает претензии из БД с фильтрацией."""
        repo = ClaimsRepository(session)
        items = await repo.get_filtered(
            date_from=date_from,
            date_to=date_to,
            status=status,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "claim_id": c.claim_id,
                    "created_date": c.created_date.isoformat() if c.created_date else None,
                    "state": c.state,
                    "text": c.text,
                    "user_name": c.user_name,
                    "answer_text": c.answer_text,
                }
                for c in items
            ],
            "count": len(items),
        }
