"""Репозиторий: Тарифы WB — комиссии, короба, паллеты, поставки."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.references import WbTariffCommission, WbTariffBox, WbTariffPallet, WbTariffSupply
from src.schemas.tariffs.tariffs import (
    CommissionCategory, BoxTariffItem, PalletTariffItem, SupplyTariffItem,
)

# asyncpg допускает не более 32767 параметров в одном запросе.
_MAX_PG_PARAMS = 32_000


class TariffsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _batched_upsert(
        self,
        model: Any,
        rows: list[dict],
        index_elements: list[str],
        update_set: dict,
    ) -> int:
        """Выполняет upsert батчами, чтобы не превысить лимит параметров PostgreSQL."""
        if not rows:
            return 0
        cols = len(rows[0])
        batch_size = max(1, _MAX_PG_PARAMS // max(cols, 1))
        total = 0
        for i in range(0, len(rows), batch_size):
            batch = rows[i: i + batch_size]
            stmt = insert(model).values(batch)
            stmt = stmt.on_conflict_do_update(index_elements=index_elements, set_=update_set(stmt))
            await self._session.execute(stmt)
            total += len(batch)
        await self._session.commit()
        return total

    # ── Комиссии ────────────────────────────────────────────────────────────────

    async def upsert_commissions(self, items: list[CommissionCategory]) -> int:
        if not items:
            return 0
        rows = [
            {
                "subject_id": item.subjectId,
                "subject_name": item.subjectName,
                "parent_name": item.parentName,
                "kgvp_marketplace": item.kgvpMarketplace,
                "kgvp_supplier": item.kgvpSupplier,
                "kgvp_supplier_express": item.kgvpSupplierExpress,
                "return_cost": item.returnCost,
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        return await self._batched_upsert(
            model=WbTariffCommission,
            rows=rows,
            index_elements=["subject_id"],
            update_set=lambda stmt: {
                "subject_name": stmt.excluded.subject_name,
                "parent_name": stmt.excluded.parent_name,
                "kgvp_marketplace": stmt.excluded.kgvp_marketplace,
                "kgvp_supplier": stmt.excluded.kgvp_supplier,
                "kgvp_supplier_express": stmt.excluded.kgvp_supplier_express,
                "return_cost": stmt.excluded.return_cost,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )

    async def count_commissions(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbTariffCommission))
        return result.scalar_one()

    async def get_all_commissions(self, limit: int = 500, offset: int = 0) -> list[WbTariffCommission]:
        result = await self._session.execute(
            select(WbTariffCommission).order_by(WbTariffCommission.subject_id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # ── Тарифы коробами ─────────────────────────────────────────────────────────

    async def upsert_box_tariffs(self, items: list[BoxTariffItem]) -> int:
        if not items:
            return 0
        rows = [
            {
                "warehouse_name": item.warehouseName,
                "box_delivery_base": float(item.boxDeliveryBase) if item.boxDeliveryBase is not None else None,
                "box_delivery_liter": float(item.boxDeliveryLiter) if item.boxDeliveryLiter is not None else None,
                "box_storage_base": float(item.boxStorageBase) if item.boxStorageBase is not None else None,
                "box_storage_liter": float(item.boxStorageLiter) if item.boxStorageLiter is not None else None,
                "fetched_at": datetime.utcnow(),
            }
            for item in items
            if item.warehouseName  # skip items without name
        ]
        return await self._batched_upsert(
            model=WbTariffBox,
            rows=rows,
            index_elements=["warehouse_name"],
            update_set=lambda stmt: {
                "box_delivery_base": stmt.excluded.box_delivery_base,
                "box_delivery_liter": stmt.excluded.box_delivery_liter,
                "box_storage_base": stmt.excluded.box_storage_base,
                "box_storage_liter": stmt.excluded.box_storage_liter,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )

    async def count_box_tariffs(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbTariffBox))
        return result.scalar_one()

    async def get_all_box_tariffs(self, limit: int = 500, offset: int = 0) -> list[WbTariffBox]:
        result = await self._session.execute(
            select(WbTariffBox).order_by(WbTariffBox.warehouse_name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # ── Тарифы паллетами ─────────────────────────────────────────────────────────

    async def upsert_pallet_tariffs(self, items: list[PalletTariffItem]) -> int:
        if not items:
            return 0
        rows = [
            {
                "warehouse_name": item.warehouseName,
                "is_super_safe": item.isSuperSafe,
                "pallet_delivery_value_base": float(item.palletDeliveryValueBase) if item.palletDeliveryValueBase is not None else None,
                "pallet_delivery_value_liter": float(item.palletDeliveryValueLiter) if item.palletDeliveryValueLiter is not None else None,
                "pallet_storage_value": float(item.palletStorageValueExpr) if item.palletStorageValueExpr is not None else None,
                "fetched_at": datetime.utcnow(),
            }
            for item in items
            if item.warehouseName  # skip items without name
        ]
        return await self._batched_upsert(
            model=WbTariffPallet,
            rows=rows,
            index_elements=["warehouse_name"],
            update_set=lambda stmt: {
                "is_super_safe": stmt.excluded.is_super_safe,
                "pallet_delivery_value_base": stmt.excluded.pallet_delivery_value_base,
                "pallet_delivery_value_liter": stmt.excluded.pallet_delivery_value_liter,
                "pallet_storage_value": stmt.excluded.pallet_storage_value,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )

    async def count_pallet_tariffs(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbTariffPallet))
        return result.scalar_one()

    async def get_all_pallet_tariffs(self, limit: int = 500, offset: int = 0) -> list[WbTariffPallet]:
        result = await self._session.execute(
            select(WbTariffPallet).order_by(WbTariffPallet.warehouse_name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # ── Тарифы на поставку (коэффициенты приёмки) ────────────────────────────────

    async def upsert_supply_tariffs(self, items: list[SupplyTariffItem]) -> int:
        """Upsert коэффициентов приёмки. Truncate + insert (нет уникального ключа для ON CONFLICT)."""
        if not items:
            return 0
        # Truncate old data and insert fresh (supply tariffs are a full snapshot)
        await self._session.execute(WbTariffSupply.__table__.delete())
        rows = [
            {
                "warehouse_id": item.warehouseID,
                "warehouse_name": item.warehouseName,
                "date": item.date,
                "coefficient": item.coefficient,
                "allow_unload": item.allowUnload,
                "box_type_id": item.boxTypeID,
                "fetched_at": datetime.utcnow(),
            }
            for item in items
            if item.warehouseID is not None
        ]
        # Batch insert
        batch_size = max(1, _MAX_PG_PARAMS // max(len(rows[0]), 1)) if rows else 0
        for i in range(0, len(rows), batch_size or 1):
            batch = rows[i: i + (batch_size or len(rows))]
            await self._session.execute(WbTariffSupply.__table__.insert(), batch)
        await self._session.commit()
        return len(rows)

    async def count_supply_tariffs(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbTariffSupply))
        return result.scalar_one()

    async def get_all_supply_tariffs(self, limit: int = 500, offset: int = 0) -> list[WbTariffSupply]:
        result = await self._session.execute(
            select(WbTariffSupply).order_by(WbTariffSupply.warehouse_name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
