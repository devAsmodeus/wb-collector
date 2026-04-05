"""Сервис DB: FBS — Чтение пропусков из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbs.passes import FbsPassesRepository
from src.services.base import BaseService


class FbsPassesDbService(BaseService):

    async def get_passes(
        self,
        session: AsyncSession,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        repo = FbsPassesRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(status=status, limit=limit, offset=offset)
        return {
            "data": [
                {
                    "pass_id":        p.pass_id,
                    "warehouse_id":   p.warehouse_id,
                    "warehouse_name": p.warehouse_name,
                    "status":         p.status,
                    "date_start":     p.date_start.isoformat() if p.date_start else None,
                    "date_end":       p.date_end.isoformat() if p.date_end else None,
                    "first_name":     p.first_name,
                    "last_name":      p.last_name,
                    "car_model":      p.car_model,
                    "car_number":     p.car_number,
                    "fetched_at":     p.fetched_at.isoformat() if p.fetched_at else None,
                }
                for p in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
