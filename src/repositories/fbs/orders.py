"""Репозиторий: Сборочные задания FBS."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import FbsOrder


class FbsOrdersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, orders: list[dict]) -> int:
        """Вставляет или обновляет заказы FBS. Возвращает кол-во обработанных записей."""
        if not orders:
            return 0
        rows = [
            {
                "order_id": o.get("orderId") or o.get("id") or o.get("order_id"),
                "order_uid": o.get("orderUID") or o.get("orderUid") or o.get("order_uid"),
                "rid": o.get("rid"),
                "date": o.get("date") or o.get("createdAt"),
                "last_change_date": o.get("lastChangeDate") or o.get("last_change_date"),
                "warehouse_name": o.get("warehouseName") or o.get("warehouse_name"),
                "country_name": o.get("countryName") or o.get("country_name"),
                "oblast_okrug_name": o.get("oblastOkrugName") or o.get("oblast_okrug_name"),
                "region_name": o.get("regionName") or o.get("region_name"),
                "article": o.get("article"),
                "nm_id": o.get("nmId") or o.get("nm_id"),
                "chrt_id": o.get("chrtId") or o.get("chrt_id"),
                "subject": o.get("subject"),
                "category": o.get("category"),
                "brand": o.get("brand"),
                "name": o.get("name"),
                "tech_size": o.get("techSize") or o.get("tech_size"),
                "color_code": o.get("colorCode") or o.get("color_code"),
                "total_price": o.get("totalPrice") or o.get("total_price"),
                "discount_percent": o.get("discountPercent") or o.get("discount_percent"),
                "spp": o.get("spp"),
                "finished_price": o.get("finishedPrice") or o.get("finished_price"),
                "price_with_disc": o.get("priceWithDisc") or o.get("price_with_disc"),
                "is_cancel": o.get("isCancel", False) or o.get("is_cancel", False),
                "cancel_date": o.get("cancelDate") or o.get("cancel_date"),
                "order_type": o.get("orderType") or o.get("order_type"),
                "supplier_status": o.get("supplierStatus") or o.get("supplier_status"),
                "wb_status": o.get("wbStatus") or o.get("wb_status"),
                "skus": o.get("skus"),
                "is_zero_order": o.get("isZeroOrder", False) or o.get("is_zero_order", False),
                "fetched_at": datetime.utcnow(),
            }
            for o in orders
        ]
        stmt = insert(FbsOrder).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["order_id"],
            set_={
                "order_uid": stmt.excluded.order_uid,
                "rid": stmt.excluded.rid,
                "date": stmt.excluded.date,
                "last_change_date": stmt.excluded.last_change_date,
                "warehouse_name": stmt.excluded.warehouse_name,
                "country_name": stmt.excluded.country_name,
                "oblast_okrug_name": stmt.excluded.oblast_okrug_name,
                "region_name": stmt.excluded.region_name,
                "article": stmt.excluded.article,
                "nm_id": stmt.excluded.nm_id,
                "chrt_id": stmt.excluded.chrt_id,
                "subject": stmt.excluded.subject,
                "category": stmt.excluded.category,
                "brand": stmt.excluded.brand,
                "name": stmt.excluded.name,
                "tech_size": stmt.excluded.tech_size,
                "color_code": stmt.excluded.color_code,
                "total_price": stmt.excluded.total_price,
                "discount_percent": stmt.excluded.discount_percent,
                "spp": stmt.excluded.spp,
                "finished_price": stmt.excluded.finished_price,
                "price_with_disc": stmt.excluded.price_with_disc,
                "is_cancel": stmt.excluded.is_cancel,
                "cancel_date": stmt.excluded.cancel_date,
                "order_type": stmt.excluded.order_type,
                "supplier_status": stmt.excluded.supplier_status,
                "wb_status": stmt.excluded.wb_status,
                "skus": stmt.excluded.skus,
                "is_zero_order": stmt.excluded.is_zero_order,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[FbsOrder]:
        """Возвращает заказы FBS из БД (последние сначала)."""
        result = await self._session.execute(
            select(FbsOrder).order_by(FbsOrder.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[FbsOrder]:
        """Возвращает заказы FBS с фильтрацией."""
        query = select(FbsOrder)
        if date_from:
            query = query.where(FbsOrder.date >= date_from)
        if date_to:
            query = query.where(FbsOrder.date <= date_to)
        if status:
            query = query.where(FbsOrder.supplier_status == status)
        query = query.order_by(FbsOrder.date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
