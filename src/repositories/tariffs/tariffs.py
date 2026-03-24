"""Репозиторий: Тарифы WB — комиссии, короба, паллеты, поставки."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.references import WbTariffCommission, WbTariffBox, WbTariffPallet, WbTariffSupply


class TariffsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # ── Комиссии ────────────────────────────────────────────────────────────────

    async def upsert_commissions(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "subject_id": item.get("subjectID"),
                "subject_name": item.get("subjectName"),
                "parent_name": item.get("parentName"),
                "kgvp_marketplace": item.get("kgvpMarketplace"),
                "kgvp_supplier": item.get("kgvpSupplier"),
                "kgvp_supplier_express": item.get("kgvpSupplierExpress"),
                "return_cost": item.get("returnCost"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbTariffCommission).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["subject_id"],
            set_={
                "subject_name": stmt.excluded.subject_name,
                "parent_name": stmt.excluded.parent_name,
                "kgvp_marketplace": stmt.excluded.kgvp_marketplace,
                "kgvp_supplier": stmt.excluded.kgvp_supplier,
                "kgvp_supplier_express": stmt.excluded.kgvp_supplier_express,
                "return_cost": stmt.excluded.return_cost,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all_commissions(self, limit: int = 500, offset: int = 0) -> list[WbTariffCommission]:
        result = await self._session.execute(
            select(WbTariffCommission).order_by(WbTariffCommission.subject_id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # ── Тарифы коробами ─────────────────────────────────────────────────────────

    async def upsert_box_tariffs(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "warehouse_id": item.get("warehouseID") or item.get("warehouse_id"),
                "warehouse_name": item.get("warehouseName") or item.get("warehouse_name"),
                "dt_next_box": item.get("dtNextBox"),
                "box_delivery_base": item.get("boxDeliveryBase"),
                "box_delivery_liter": item.get("boxDeliveryLiter"),
                "box_delivery_additional_liter": item.get("boxDeliveryAdditionalLiter"),
                "box_storage_base": item.get("boxStorageBase"),
                "box_storage_liter": item.get("boxStorageLiter"),
                "box_storage_additional_liter": item.get("boxStorageAdditionalLiter"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbTariffBox).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["warehouse_id"],
            set_={
                "warehouse_name": stmt.excluded.warehouse_name,
                "dt_next_box": stmt.excluded.dt_next_box,
                "box_delivery_base": stmt.excluded.box_delivery_base,
                "box_delivery_liter": stmt.excluded.box_delivery_liter,
                "box_delivery_additional_liter": stmt.excluded.box_delivery_additional_liter,
                "box_storage_base": stmt.excluded.box_storage_base,
                "box_storage_liter": stmt.excluded.box_storage_liter,
                "box_storage_additional_liter": stmt.excluded.box_storage_additional_liter,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all_box_tariffs(self, limit: int = 500, offset: int = 0) -> list[WbTariffBox]:
        result = await self._session.execute(
            select(WbTariffBox).order_by(WbTariffBox.warehouse_name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # ── Тарифы паллетами ─────────────────────────────────────────────────────────

    async def upsert_pallet_tariffs(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "warehouse_id": item.get("warehouseID") or item.get("warehouse_id"),
                "warehouse_name": item.get("warehouseName") or item.get("warehouse_name"),
                "is_super_safe": item.get("isSuperSafe"),
                "pallet_delivery_value_base": item.get("palletDeliveryValueBase"),
                "pallet_delivery_value_liter": item.get("palletDeliveryValueLiter"),
                "pallet_storage_value": item.get("palletStorageValue"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbTariffPallet).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["warehouse_id"],
            set_={
                "warehouse_name": stmt.excluded.warehouse_name,
                "is_super_safe": stmt.excluded.is_super_safe,
                "pallet_delivery_value_base": stmt.excluded.pallet_delivery_value_base,
                "pallet_delivery_value_liter": stmt.excluded.pallet_delivery_value_liter,
                "pallet_storage_value": stmt.excluded.pallet_storage_value,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all_pallet_tariffs(self, limit: int = 500, offset: int = 0) -> list[WbTariffPallet]:
        result = await self._session.execute(
            select(WbTariffPallet).order_by(WbTariffPallet.warehouse_name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    # ── Тарифы на поставку ───────────────────────────────────────────────────────

    async def upsert_supply_tariffs(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "warehouse_id": item.get("warehouseID") or item.get("warehouse_id"),
                "warehouse_name": item.get("warehouseName") or item.get("warehouse_name"),
                "coefficient": item.get("coefficient"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbTariffSupply).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["warehouse_id"],
            set_={
                "warehouse_name": stmt.excluded.warehouse_name,
                "coefficient": stmt.excluded.coefficient,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all_supply_tariffs(self, limit: int = 500, offset: int = 0) -> list[WbTariffSupply]:
        result = await self._session.execute(
            select(WbTariffSupply).order_by(WbTariffSupply.warehouse_name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
