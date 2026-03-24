"""Репозиторий: Претензии покупателей."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.communications import WbClaim


class ClaimsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, claims: list[dict]) -> int:
        """Вставляет или обновляет претензии. Возвращает кол-во обработанных записей."""
        if not claims:
            return 0
        rows = [
            {
                "claim_id": c.get("id", ""),
                "created_date": datetime.fromisoformat(c["createdDate"]) if c.get("createdDate") else None,
                "state": c.get("status"),
                "text": c.get("text"),
                "user_name": c.get("userName"),
                "answer_text": c.get("answer", {}).get("text") if c.get("answer") else None,
                "product_details": c.get("productDetails"),
                "fetched_at": datetime.utcnow(),
            }
            for c in claims
        ]
        stmt = insert(WbClaim).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["claim_id"],
            set_={
                "created_date": stmt.excluded.created_date,
                "state": stmt.excluded.state,
                "text": stmt.excluded.text,
                "user_name": stmt.excluded.user_name,
                "answer_text": stmt.excluded.answer_text,
                "product_details": stmt.excluded.product_details,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbClaim]:
        """Возвращает претензии из БД (последние сначала)."""
        result = await self._session.execute(
            select(WbClaim).order_by(WbClaim.created_date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[WbClaim]:
        """Возвращает претензии с фильтрацией по параметрам."""
        query = select(WbClaim)
        if date_from:
            query = query.where(WbClaim.created_date >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.where(WbClaim.created_date <= datetime.fromisoformat(date_to))
        if status is not None:
            query = query.where(WbClaim.state == status)
        query = query.order_by(WbClaim.created_date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
