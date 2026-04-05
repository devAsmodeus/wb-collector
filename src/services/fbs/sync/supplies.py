"""Сервис Sync: FBS — Синхронизация поставок FBS."""
import logging
from datetime import datetime
from dateutil.parser import isoparse
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.fbs.supplies import SuppliesCollector
from src.models.orders import FbsSupply
from src.services.base import BaseService

logger = logging.getLogger(__name__)


def _parse_dt(val) -> datetime | None:
    if not val:
        return None
    try:
        return isoparse(str(val)).replace(tzinfo=None)
    except Exception:
        return None


class FbsSuppliesSyncService(BaseService):

    async def sync_supplies(self, session: AsyncSession) -> dict:
        async with SuppliesCollector() as collector:
            all_supplies = []
            limit = 1000
            offset = 0
            while True:
                response = await collector.get_supplies(limit=limit, offset=offset)
                supplies = response.supplies if hasattr(response, 'supplies') else []
                if not supplies:
                    break
                all_supplies.extend(supplies)
                new_next = getattr(response, 'next', None)
                if not new_next or new_next == offset or len(supplies) < limit:
                    break
                offset = new_next

        if not all_supplies:
            return {"synced": 0}

        rows = [
            {
                "supply_id":             s.id if hasattr(s, 'id') else (s.supplyId or ''),
                "name":                  getattr(s, 'name', None),
                "is_b2b":                getattr(s, 'isB2b', None),
                "done":                  getattr(s, 'done', None),
                "cargo_type":            getattr(s, 'cargoType', None),
                "cross_border_type":     getattr(s, 'crossBorderType', None),
                "destination_office_id": getattr(s, 'destinationOfficeId', None),
                "created_at":            _parse_dt(getattr(s, 'createdAt', None)),
                "closed_at":             _parse_dt(getattr(s, 'closedAt', None)),
                "scan_dt":               _parse_dt(getattr(s, 'scanDt', None)),
                "fetched_at":            datetime.utcnow(),
            }
            for s in all_supplies if (getattr(s, 'id', None) or getattr(s, 'supplyId', None))
        ]

        if not rows:
            return {"synced": 0}

        stmt = insert(FbsSupply).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["supply_id"],
            set_={k: getattr(stmt.excluded, k) for k in rows[0] if k != "supply_id"},
        )
        await session.execute(stmt)
        await session.commit()

        logger.info(f"FBS supplies synced: {len(rows)}")
        return {"synced": len(rows)}
