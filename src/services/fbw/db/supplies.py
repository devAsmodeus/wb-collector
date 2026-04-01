"""Сервис DB: FBW — Чтение поставок и товаров из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbw.supplies import FbwSuppliesRepository, FbwSupplyGoodsRepository
from src.services.base import BaseService


class FbwSuppliesDbService(BaseService):

    async def get_supplies(
        self, session: AsyncSession, limit: int = 100, offset: int = 0,
    ) -> dict:
        """Возвращает поставки FBW из БД с пагинацией."""
        repo = FbwSuppliesRepository(session)
        total = await repo.count()
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "supply_id": s.supply_id,
                    "preorder_id": s.preorder_id,
                    "status_id": s.status_id,
                    "box_type_id": s.box_type_id,
                    "is_box_on_pallet": s.is_box_on_pallet,
                    "create_date": s.create_date.isoformat() if s.create_date else None,
                    "supply_date": s.supply_date.isoformat() if s.supply_date else None,
                    "fact_date": s.fact_date.isoformat() if s.fact_date else None,
                    "updated_date": s.updated_date.isoformat() if s.updated_date else None,
                    "phone": s.phone,
                    "fetched_at": s.fetched_at.isoformat() if s.fetched_at else None,
                }
                for s in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_supply(self, session: AsyncSession, supply_id: int) -> dict | None:
        """Возвращает одну поставку FBW по supply_id с товарами."""
        supply_repo = FbwSuppliesRepository(session)
        goods_repo = FbwSupplyGoodsRepository(session)

        supply = await supply_repo.get_by_id(supply_id)
        if not supply:
            return None

        goods = await goods_repo.get_by_supply_id(supply_id)

        return {
            "supply_id": supply.supply_id,
            "preorder_id": supply.preorder_id,
            "status_id": supply.status_id,
            "box_type_id": supply.box_type_id,
            "is_box_on_pallet": supply.is_box_on_pallet,
            "create_date": supply.create_date.isoformat() if supply.create_date else None,
            "supply_date": supply.supply_date.isoformat() if supply.supply_date else None,
            "fact_date": supply.fact_date.isoformat() if supply.fact_date else None,
            "updated_date": supply.updated_date.isoformat() if supply.updated_date else None,
            "phone": supply.phone,
            "raw_data": supply.raw_data,
            "fetched_at": supply.fetched_at.isoformat() if supply.fetched_at else None,
            "goods": [
                {
                    "barcode": g.barcode,
                    "vendor_code": g.vendor_code,
                    "name": g.name,
                    "quantity": g.quantity,
                    "brand": g.brand,
                    "subject": g.subject,
                }
                for g in goods
            ],
        }

    async def get_supply_goods(
        self, session: AsyncSession, supply_id: int, limit: int = 1000, offset: int = 0,
    ) -> dict:
        """Возвращает товары поставки FBW из БД с пагинацией."""
        repo = FbwSupplyGoodsRepository(session)
        total = await repo.count_by_supply_id(supply_id)
        items = await repo.get_by_supply_id(supply_id, limit=limit, offset=offset)
        return {
            "data": [
                {
                    "supply_id": g.supply_id,
                    "barcode": g.barcode,
                    "vendor_code": g.vendor_code,
                    "name": g.name,
                    "quantity": g.quantity,
                    "brand": g.brand,
                    "subject": g.subject,
                    "fetched_at": g.fetched_at.isoformat() if g.fetched_at else None,
                }
                for g in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
