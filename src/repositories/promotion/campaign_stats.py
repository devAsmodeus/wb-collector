"""Репозиторий: Статистика рекламных кампаний WB."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.promotion import WbCampaignStat


class CampaignStatsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, stats: list[dict]) -> int:
        """Вставляет или обновляет статистику кампаний. Возвращает кол-во обработанных записей."""
        if not stats:
            return 0
        def _parse_date(val):
            if val is None:
                return None
            if isinstance(val, datetime):
                return val.replace(tzinfo=None) if val.tzinfo else val
            try:
                dt = datetime.fromisoformat(str(val).replace("Z", "+00:00"))
                return dt.replace(tzinfo=None)
            except (ValueError, TypeError):
                return None

        rows = [
            {
                "advert_id": s.get("advertId") or s.get("advert_id"),
                "date": _parse_date(s.get("date")),
                "views": s.get("views"),
                "clicks": s.get("clicks"),
                "ctr": s.get("ctr"),
                "cpc": s.get("cpc"),
                "sum": s.get("sum"),
                "atbs": s.get("atbs"),
                "orders": s.get("orders"),
                "cr": s.get("cr"),
                "shks": s.get("shks"),
                "sum_price": s.get("sum_price") or s.get("sumPrice"),
                "raw_data": s.get("raw_data"),
                "fetched_at": datetime.utcnow(),
            }
            for s in stats
        ]
        stmt = insert(WbCampaignStat).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_campaign_stats_advert_date",
            set_={
                "views": stmt.excluded.views,
                "clicks": stmt.excluded.clicks,
                "ctr": stmt.excluded.ctr,
                "cpc": stmt.excluded.cpc,
                "sum": stmt.excluded.sum,
                "atbs": stmt.excluded.atbs,
                "orders": stmt.excluded.orders,
                "cr": stmt.excluded.cr,
                "shks": stmt.excluded.shks,
                "sum_price": stmt.excluded.sum_price,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_date(self) -> datetime | None:
        """Возвращает максимальную дату статистики кампании из БД."""
        result = await self._session.execute(select(func.max(WbCampaignStat.date)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество записей статистики кампаний в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbCampaignStat))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbCampaignStat]:
        """Возвращает статистику с пагинацией."""
        result = await self._session.execute(
            select(WbCampaignStat).order_by(WbCampaignStat.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_campaign(self, advert_id: int, limit: int = 100, offset: int = 0) -> list[WbCampaignStat]:
        """Возвращает статистику по конкретной кампании."""
        result = await self._session.execute(
            select(WbCampaignStat)
            .where(WbCampaignStat.advert_id == advert_id)
            .order_by(WbCampaignStat.date.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
