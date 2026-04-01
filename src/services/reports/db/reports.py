"""Сервис DB: Отчёты — Чтение остатков, заказов, продаж из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.reports.stocks import StocksRepository
from src.repositories.reports.order_reports import OrderReportsRepository
from src.repositories.reports.sale_reports import SaleReportsRepository
from src.services.base import BaseService


class ReportsDbService(BaseService):

    async def get_stocks(self, session: AsyncSession, date_from=None, date_to=None, limit=500, offset=0) -> dict:
        repo = StocksRepository(session)
        total = await repo.count()
        if date_from or date_to:
            items = await repo.get_filtered(date_from=date_from, date_to=date_to, limit=limit, offset=offset)
        else:
            items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "nm_id": s.nm_id,
                    "supplier_article": s.supplier_article,
                    "barcode": s.barcode,
                    "warehouse_name": s.warehouse_name,
                    "quantity": s.quantity,
                    "quantity_full": s.quantity_full,
                    "in_way_to_client": s.in_way_to_client,
                    "in_way_from_client": s.in_way_from_client,
                    "subject": s.subject,
                    "category": s.category,
                    "brand": s.brand,
                    "price": float(s.price) if s.price else None,
                    "last_change_date": s.last_change_date.isoformat() if s.last_change_date else None,
                    "fetched_at": s.fetched_at.isoformat() if s.fetched_at else None,
                }
                for s in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_orders(self, session: AsyncSession, date_from=None, date_to=None, limit=500, offset=0) -> dict:
        repo = OrderReportsRepository(session)
        total = await repo.count()
        if date_from or date_to:
            items = await repo.get_filtered(date_from=date_from, date_to=date_to, limit=limit, offset=offset)
        else:
            items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "odid": o.odid,
                    "nm_id": o.nm_id,
                    "supplier_article": o.supplier_article,
                    "barcode": o.barcode,
                    "warehouse_name": o.warehouse_name,
                    "oblast": o.oblast,
                    "total_price": float(o.total_price) if o.total_price else None,
                    "discount_percent": float(o.discount_percent) if o.discount_percent else None,
                    "subject": o.subject,
                    "category": o.category,
                    "brand": o.brand,
                    "is_cancel": o.is_cancel,
                    "date": o.date.isoformat() if o.date else None,
                    "fetched_at": o.fetched_at.isoformat() if o.fetched_at else None,
                }
                for o in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_sales(self, session: AsyncSession, date_from=None, date_to=None, limit=500, offset=0) -> dict:
        repo = SaleReportsRepository(session)
        total = await repo.count()
        if date_from or date_to:
            items = await repo.get_filtered(date_from=date_from, date_to=date_to, limit=limit, offset=offset)
        else:
            items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "srid": s.srid,
                    "sale_id": s.sale_id,
                    "nm_id": s.nm_id,
                    "supplier_article": s.supplier_article,
                    "barcode": s.barcode,
                    "warehouse_name": s.warehouse_name,
                    "oblast": s.oblast,
                    "total_price": float(s.total_price) if s.total_price else None,
                    "discount_percent": float(s.discount_percent) if s.discount_percent else None,
                    "subject": s.subject,
                    "category": s.category,
                    "brand": s.brand,
                    "date": s.date.isoformat() if s.date else None,
                    "fetched_at": s.fetched_at.isoformat() if s.fetched_at else None,
                }
                for s in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
