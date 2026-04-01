"""Сервис DB: Тарифы — Чтение тарифов WB из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.tariffs.tariffs import TariffsRepository
from src.services.base import BaseService


class TariffsDbService(BaseService):

    async def get_commissions(self, session: AsyncSession, limit: int = 500, offset: int = 0) -> dict:
        repo = TariffsRepository(session)
        total = await repo.count_commissions()
        items = await repo.get_all_commissions(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "subject_id": t.subject_id,
                    "subject_name": t.subject_name,
                    "parent_name": t.parent_name,
                    "kgvp_marketplace": float(t.kgvp_marketplace) if t.kgvp_marketplace else None,
                    "kgvp_supplier": float(t.kgvp_supplier) if t.kgvp_supplier else None,
                    "kgvp_supplier_express": float(t.kgvp_supplier_express) if t.kgvp_supplier_express else None,
                    "return_cost": float(t.return_cost) if t.return_cost else None,
                    "fetched_at": t.fetched_at.isoformat() if t.fetched_at else None,
                }
                for t in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_box_tariffs(self, session: AsyncSession, limit: int = 500, offset: int = 0) -> dict:
        repo = TariffsRepository(session)
        total = await repo.count_box_tariffs()
        items = await repo.get_all_box_tariffs(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "warehouse_name": t.warehouse_name,
                    "box_delivery_base": float(t.box_delivery_base) if t.box_delivery_base else None,
                    "box_delivery_liter": float(t.box_delivery_liter) if t.box_delivery_liter else None,
                    "box_storage_base": float(t.box_storage_base) if t.box_storage_base else None,
                    "box_storage_liter": float(t.box_storage_liter) if t.box_storage_liter else None,
                    "fetched_at": t.fetched_at.isoformat() if t.fetched_at else None,
                }
                for t in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_pallet_tariffs(self, session: AsyncSession, limit: int = 500, offset: int = 0) -> dict:
        repo = TariffsRepository(session)
        total = await repo.count_pallet_tariffs()
        items = await repo.get_all_pallet_tariffs(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "warehouse_name": t.warehouse_name,
                    "is_super_safe": t.is_super_safe,
                    "pallet_delivery_value_base": float(t.pallet_delivery_value_base) if t.pallet_delivery_value_base else None,
                    "pallet_delivery_value_liter": float(t.pallet_delivery_value_liter) if t.pallet_delivery_value_liter else None,
                    "pallet_storage_value": float(t.pallet_storage_value) if t.pallet_storage_value else None,
                    "fetched_at": t.fetched_at.isoformat() if t.fetched_at else None,
                }
                for t in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_supply_tariffs(self, session: AsyncSession, limit: int = 500, offset: int = 0) -> dict:
        repo = TariffsRepository(session)
        total = await repo.count_supply_tariffs()
        items = await repo.get_all_supply_tariffs(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "warehouse_id": t.warehouse_id,
                    "warehouse_name": t.warehouse_name,
                    "coefficient": t.coefficient,
                    "fetched_at": t.fetched_at.isoformat() if t.fetched_at else None,
                }
                for t in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
