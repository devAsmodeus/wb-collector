"""Репозиторий: Поставки FBW и товары в поставках."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.fbw import FbwSupply, FbwSupplyGood


class FbwSuppliesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        """Вставляет или обновляет поставки FBW. Возвращает кол-во обработанных записей."""
        if not items:
            return 0
        rows = [
            {
                "supply_id": item["supply_id"],
                "preorder_id": item.get("preorder_id"),
                "status_id": item.get("status_id"),
                "box_type_id": item.get("box_type_id"),
                "is_box_on_pallet": item.get("is_box_on_pallet"),
                "create_date": item.get("create_date"),
                "supply_date": item.get("supply_date"),
                "fact_date": item.get("fact_date"),
                "updated_date": item.get("updated_date"),
                "phone": item.get("phone"),
                "raw_data": item.get("raw_data"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(FbwSupply).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["supply_id"],
            set_={
                "preorder_id": stmt.excluded.preorder_id,
                "status_id": stmt.excluded.status_id,
                "box_type_id": stmt.excluded.box_type_id,
                "is_box_on_pallet": stmt.excluded.is_box_on_pallet,
                "create_date": stmt.excluded.create_date,
                "supply_date": stmt.excluded.supply_date,
                "fact_date": stmt.excluded.fact_date,
                "updated_date": stmt.excluded.updated_date,
                "phone": stmt.excluded.phone,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_updated_date(self) -> datetime | None:
        """Возвращает максимальную дату обновления поставки для инкрементальной синхронизации."""
        result = await self._session.execute(select(func.max(FbwSupply.updated_date)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество поставок FBW в БД."""
        result = await self._session.execute(select(func.count()).select_from(FbwSupply))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[FbwSupply]:
        """Возвращает поставки FBW с пагинацией."""
        result = await self._session.execute(
            select(FbwSupply).order_by(FbwSupply.supply_id.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_id(self, supply_id: int) -> FbwSupply | None:
        """Возвращает поставку по supply_id."""
        result = await self._session.execute(
            select(FbwSupply).where(FbwSupply.supply_id == supply_id)
        )
        return result.scalars().one_or_none()


class FbwSupplyGoodsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        """Вставляет или обновляет товары в поставках FBW. Возвращает кол-во обработанных записей."""
        if not items:
            return 0
        rows = [
            {
                "supply_id": item["supply_id"],
                "barcode": item.get("barcode"),
                "vendor_code": item.get("vendor_code"),
                "name": item.get("name"),
                "quantity": item.get("quantity"),
                "brand": item.get("brand"),
                "subject": item.get("subject"),
                "raw_data": item.get("raw_data"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(FbwSupplyGood).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_fbw_supply_good",
            set_={
                "vendor_code": stmt.excluded.vendor_code,
                "name": stmt.excluded.name,
                "quantity": stmt.excluded.quantity,
                "brand": stmt.excluded.brand,
                "subject": stmt.excluded.subject,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        """Возвращает общее количество товаров в поставках FBW."""
        result = await self._session.execute(select(func.count()).select_from(FbwSupplyGood))
        return result.scalar_one()

    async def get_by_supply_id(self, supply_id: int, limit: int = 1000, offset: int = 0) -> list[FbwSupplyGood]:
        """Возвращает товары поставки по supply_id."""
        result = await self._session.execute(
            select(FbwSupplyGood)
            .where(FbwSupplyGood.supply_id == supply_id)
            .order_by(FbwSupplyGood.id)
            .limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def count_by_supply_id(self, supply_id: int) -> int:
        """Возвращает количество товаров в конкретной поставке."""
        result = await self._session.execute(
            select(func.count()).select_from(FbwSupplyGood).where(FbwSupplyGood.supply_id == supply_id)
        )
        return result.scalar_one()
