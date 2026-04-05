"""Репозиторий: Претензии покупателей."""
from datetime import datetime

from sqlalchemy import select, func
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
                "created_date": datetime.fromisoformat(c["dt"]) if c.get("dt") else None,
                "state": str(c.get("status")) if c.get("status") is not None else None,
                "text": c.get("user_comment"),
                "user_name": c.get("imt_name"),
                "answer_text": c.get("wb_comment"),
                "product_details": {
                    "nm_id": c.get("nm_id"),
                    "price": c.get("price"),
                    "claim_type": c.get("claim_type"),
                    "photos": c.get("photos"),
                    "video_paths": c.get("video_paths"),
                    "actions": c.get("actions"),
                    "srid": c.get("srid"),
                    "order_dt": c.get("order_dt"),
                    "delivery_dt": c.get("delivery_dt"),
                },
                "fetched_at": datetime.utcnow(),
            }
            for c in claims if c.get("id")
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

    async def count(self) -> int:
        """Возвращает общее количество претензий в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbClaim))
        return result.scalar_one()

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
