"""Репозиторий: Акции WB (календарь акций)."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.promotion import WbPromotion


class PromotionsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, promotions: list[dict]) -> int:
        """Вставляет или обновляет акции. Возвращает кол-во обработанных записей."""
        if not promotions:
            return 0
        rows = [
            {
                "promotion_id": p.get("id") or p.get("promotion_id"),
                "name": p.get("name"),
                "start_date": p.get("startDateTime") or p.get("start_date"),
                "end_date": p.get("endDateTime") or p.get("end_date"),
                "type": p.get("type"),
                "in_action": p.get("inAction") or p.get("in_action"),
                "fetched_at": datetime.utcnow(),
            }
            for p in promotions
        ]
        stmt = insert(WbPromotion).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["promotion_id"],
            set_={
                "name": stmt.excluded.name,
                "start_date": stmt.excluded.start_date,
                "end_date": stmt.excluded.end_date,
                "type": stmt.excluded.type,
                "in_action": stmt.excluded.in_action,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbPromotion]:
        """Возвращает акции с пагинацией."""
        result = await self._session.execute(
            select(WbPromotion).order_by(WbPromotion.start_date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
