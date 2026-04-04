"""Сервис Sync: FBS — Синхронизация пропусков на склад WB."""
import logging
from datetime import datetime
from dateutil.parser import isoparse
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.fbs.passes import PassesCollector
from src.models.orders import FbsPass
from src.services.base import BaseService

logger = logging.getLogger(__name__)


def _parse_dt(val) -> datetime | None:
    if not val:
        return None
    try:
        return isoparse(str(val)).replace(tzinfo=None)
    except Exception:
        return None


class FbsPassesSyncService(BaseService):

    async def sync_passes(self, session: AsyncSession) -> dict:
        async with PassesCollector() as collector:
            response = await collector.get_passes()
            passes = response.passes if hasattr(response, 'passes') else []

        if not passes:
            return {"synced": 0}

        rows = [
            {
                "pass_id":       p.passId,
                "warehouse_id":  p.warehouseId,
                "warehouse_name": p.warehouseName,
                "status":        p.status,
                "date_start":    _parse_dt(getattr(p, 'dateStart', None)),
                "date_end":      _parse_dt(getattr(p, 'dateEnd', None)),
                "first_name":    getattr(p, 'firstName', None),
                "last_name":     getattr(p, 'lastName', None),
                "car_model":     getattr(p, 'carModel', None),
                "car_number":    getattr(p, 'carNumber', None),
                "fetched_at":    datetime.utcnow(),
            }
            for p in passes if p.passId is not None
        ]

        if not rows:
            return {"synced": 0}

        stmt = insert(FbsPass).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["pass_id"],
            set_={k: getattr(stmt.excluded, k) for k in rows[0] if k != "pass_id"},
        )
        await session.execute(stmt)
        await session.commit()

        logger.info(f"FBS passes synced: {len(rows)}")
        return {"synced": len(rows)}
