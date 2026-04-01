"""Сервис DB: FBW — Чтение складов WB из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbw.warehouses import FbwWarehousesRepository
from src.services.base import BaseService


class FbwWarehousesDbService(BaseService):

    async def get_warehouses(
        self, session: AsyncSession, limit: int = 500, offset: int = 0,
    ) -> dict:
        """Возвращает склады WB для FBW из БД с пагинацией."""
        repo = FbwWarehousesRepository(session)
        total = await repo.count()
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "id": w.id,
                    "name": w.name,
                    "address": w.address,
                    "work_time": w.work_time,
                    "accepts_qr": w.accepts_qr,
                    "fetched_at": w.fetched_at.isoformat() if w.fetched_at else None,
                }
                for w in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
