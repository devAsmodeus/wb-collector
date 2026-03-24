"""Сервис DB: Финансы — Чтение финансовых отчётов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.finances.financial_reports import FinancialReportsRepository
from src.services.base import BaseService


class FinancesDbService(BaseService):

    async def get_financial_report(self, session: AsyncSession, date_from=None, date_to=None, limit=500, offset=0) -> dict:
        repo = FinancialReportsRepository(session)
        if date_from or date_to:
            items = await repo.get_filtered(date_from=date_from, date_to=date_to, limit=limit, offset=offset)
        else:
            items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "rrd_id": r.rrd_id,
                    "realizationreport_id": r.realizationreport_id,
                    "nm_id": r.nm_id,
                    "sa_name": r.sa_name,
                    "barcode": r.barcode,
                    "subject_name": r.subject_name,
                    "brand_name": r.brand_name,
                    "doc_type_name": r.doc_type_name,
                    "quantity": r.quantity,
                    "retail_price": float(r.retail_price) if r.retail_price else None,
                    "retail_amount": float(r.retail_amount) if r.retail_amount else None,
                    "ppvz_for_pay": float(r.ppvz_for_pay) if r.ppvz_for_pay else None,
                    "delivery_rub": float(r.delivery_rub) if r.delivery_rub else None,
                    "penalty": float(r.penalty) if r.penalty else None,
                    "storage_fee": float(r.storage_fee) if r.storage_fee else None,
                    "deduction": float(r.deduction) if r.deduction else None,
                    "order_dt": r.order_dt.isoformat() if r.order_dt else None,
                    "sale_dt": r.sale_dt.isoformat() if r.sale_dt else None,
                    "fetched_at": r.fetched_at.isoformat() if r.fetched_at else None,
                }
                for r in items
            ],
            "count": len(items),
        }
