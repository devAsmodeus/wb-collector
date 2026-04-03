"""Сервис DB: Товары — Чтение складов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.warehouses import WarehousesRepository
from src.services.base import BaseService


class WarehousesDbService(BaseService):

    async def get_warehouses(self, session: AsyncSession) -> dict:
        """Возвращает все склады продавца из БД."""
        repo = WarehousesRepository(session)
        total = await repo.count()
        items = await repo.get_all()
        return {
            "data": [
                {
                    "warehouse_id": w.warehouse_id,
                    "name": w.name,
                    "office_id": w.office_id,
                    "cargo_type": w.cargo_type,
                    "delivery_type": w.delivery_type,
                    "is_deleting": w.is_deleting,
                    "is_processing": w.is_processing,
                    "fetched_at": w.fetched_at.isoformat() if w.fetched_at else None,
                }
                for w in items
            ],
            "total": total,
            "limit": total,
            "offset": 0,
        }
