"""Репозиторий: Заказы DBW."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import DbwOrder


class DbwOrdersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, orders: list[dict]) -> int:
        """Вставляет или обновляет заказы DBW. Возвращает кол-во обработанных записей."""
        if not orders:
            return 0
        rows = [
            {
                "order_id": o.get("id") or o.get("order_id"),
                "order_uid": o.get("orderUid") or o.get("order_uid"),
                "rid": o.get("rid"),
                "date": o.get("createdAt") or o.get("date"),
                "last_change_date": o.get("lastChangeDate") or o.get("last_change_date"),
                "warehouse_name": o.get("warehouseName") or o.get("warehouse_name"),
                "country_name": o.get("countryName") or o.get("country_name"),
                "region_name": o.get("regionName") or o.get("region_name"),
                "article": o.get("article"),
                "nm_id": o.get("nmId") or o.get("nm_id"),
                "chrt_id": o.get("chrtId") or o.get("chrt_id"),
                "subject": o.get("subject"),
                "category": o.get("category"),
                "brand": o.get("brand"),
                "name": o.get("name"),
                "tech_size": o.get("techSize") or o.get("tech_size"),
                "total_price": o.get("totalPrice") or o.get("total_price"),
                "discount_percent": o.get("discountPercent") or o.get("discount_percent"),
                "finished_price": o.get("finishedPrice") or o.get("finished_price"),
                "is_cancel": o.get("isCancel", False) or o.get("is_cancel", False),
                "cancel_date": o.get("cancelDate") or o.get("cancel_date"),
                "order_type": o.get("orderType") or o.get("order_type"),
                "supplier_status": o.get("supplierStatus") or o.get("supplier_status"),
                "wb_status": o.get("wbStatus") or o.get("wb_status"),
                "fetched_at": datetime.utcnow(),
            }
            for o in orders
        ]
        stmt = insert(DbwOrder).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["order_id"],
            set_={
                "order_uid": stmt.excluded.order_uid,
                "rid": stmt.excluded.rid,
                "date": stmt.excluded.date,
                "last_change_date": stmt.excluded.last_change_date,
                "warehouse_name": stmt.excluded.warehouse_name,
                "country_name": stmt.excluded.country_name,
                "region_name": stmt.excluded.region_name,
                "article": stmt.excluded.article,
                "nm_id": stmt.excluded.nm_id,
                "chrt_id": stmt.excluded.chrt_id,
                "subject": stmt.excluded.subject,
                "category": stmt.excluded.category,
                "brand": stmt.excluded.brand,
                "name": stmt.excluded.name,
                "tech_size": stmt.excluded.tech_size,
                "total_price": stmt.excluded.total_price,
                "discount_percent": stmt.excluded.discount_percent,
                "finished_price": stmt.excluded.finished_price,
                "is_cancel": stmt.excluded.is_cancel,
                "cancel_date": stmt.excluded.cancel_date,
                "order_type": stmt.excluded.order_type,
                "supplier_status": stmt.excluded.supplier_status,
                "wb_status": stmt.excluded.wb_status,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        """Возвращает общее количество заказов DBW в БД."""
        result = await self._session.execute(select(func.count()).select_from(DbwOrder))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[DbwOrder]:
        """Возвращает заказы DBW из БД (последние сначала)."""
        result = await self._session.execute(
            select(DbwOrder).order_by(DbwOrder.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_max_date(self) -> datetime | None:
        """Возвращает максимальную дату заказа DBW в БД (для инкрементального обновления)."""
        result = await self._session.execute(
            select(func.max(DbwOrder.date))
        )
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[DbwOrder]:
        """Возвращает заказы DBW с фильтрацией."""
        query = select(DbwOrder)
        if date_from:
            query = query.where(DbwOrder.date >= date_from)
        if date_to:
            query = query.where(DbwOrder.date <= date_to)
        if status:
            query = query.where(DbwOrder.supplier_status == status)
        query = query.order_by(DbwOrder.date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
