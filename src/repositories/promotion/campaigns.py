"""Репозиторий: Рекламные кампании WB."""
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.promotion import WbCampaign


class CampaignsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, campaigns: list[dict]) -> int:
        """Вставляет или обновляет кампании. Возвращает кол-во обработанных записей."""
        if not campaigns:
            return 0

        def _parse_dt(val) -> datetime | None:
            """Конвертирует ISO-строку или datetime в datetime (naive UTC)."""
            if val is None:
                return None
            if isinstance(val, datetime):
                return val.replace(tzinfo=None) if val.tzinfo else val
            try:
                dt = datetime.fromisoformat(str(val))
                return dt.replace(tzinfo=None) if dt.tzinfo else dt
            except (ValueError, TypeError):
                return None

        rows = [
            {
                "advert_id": c.get("advertId") or c.get("advert_id"),
                "name": c.get("name"),
                "status": c.get("status"),
                "type": c.get("type"),
                "payment_type": c.get("paymentType") or c.get("payment_type"),
                "create_time": _parse_dt(c.get("createTime") or c.get("create_time")),
                "change_time": _parse_dt(c.get("changeTime") or c.get("change_time")),
                "start_time": _parse_dt(c.get("startTime") or c.get("start_time")),
                "end_time": _parse_dt(c.get("endTime") or c.get("end_time")),
                "fetched_at": datetime.utcnow(),
            }
            for c in campaigns
            if c.get("advertId") or c.get("advert_id")
        ]
        if not rows:
            return 0
        stmt = insert(WbCampaign).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["advert_id"],
            set_={
                "name": stmt.excluded.name,
                "status": stmt.excluded.status,
                "type": stmt.excluded.type,
                "payment_type": stmt.excluded.payment_type,
                "create_time": stmt.excluded.create_time,
                "change_time": stmt.excluded.change_time,
                "start_time": stmt.excluded.start_time,
                "end_time": stmt.excluded.end_time,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_change_time(self) -> datetime | None:
        """Возвращает максимальную дату изменения кампании из БД."""
        result = await self._session.execute(select(func.max(WbCampaign.change_time)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество кампаний в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbCampaign))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbCampaign]:
        """Возвращает кампании с пагинацией."""
        result = await self._session.execute(
            select(WbCampaign).order_by(WbCampaign.advert_id.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        status: int | None = None,
        type_: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[WbCampaign]:
        """Возвращает кампании с фильтрацией по статусу и типу."""
        query = select(WbCampaign)
        if status is not None:
            query = query.where(WbCampaign.status == status)
        if type_ is not None:
            query = query.where(WbCampaign.type == type_)
        query = query.order_by(WbCampaign.advert_id.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_all_ids(self) -> list[int]:
        """Возвращает все advert_id из БД."""
        from sqlalchemy import text
        result = await self._session.execute(
            select(WbCampaign.advert_id).where(WbCampaign.advert_id.isnot(None))
        )
        return [row[0] for row in result.all()]
