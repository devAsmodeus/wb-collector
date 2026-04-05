"""Сервис DB: FBS — Чтение поставок FBS из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbs.supplies import FbsSuppliesRepository
from src.services.base import BaseService


class FbsSuppliesDbService(BaseService):

    async def get_supplies(
        self,
        session: AsyncSession,
        done: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        repo = FbsSuppliesRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(done=done, limit=limit, offset=offset)
        return {
            "data": [
                {
                    "supply_id":             s.supply_id,
                    "name":                  s.name,
                    "is_b2b":                s.is_b2b,
                    "done":                  s.done,
                    "cargo_type":            s.cargo_type,
                    "cross_border_type":     s.cross_border_type,
                    "destination_office_id": s.destination_office_id,
                    "created_at":            s.created_at.isoformat() if s.created_at else None,
                    "closed_at":             s.closed_at.isoformat() if s.closed_at else None,
                    "scan_dt":               s.scan_dt.isoformat() if s.scan_dt else None,
                    "fetched_at":            s.fetched_at.isoformat() if s.fetched_at else None,
                }
                for s in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
