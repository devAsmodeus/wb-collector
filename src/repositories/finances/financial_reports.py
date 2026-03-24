"""Репозиторий: Финансовые отчёты WB."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reports import WbFinancialReport


class FinancialReportsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "rrd_id": item.get("rrd_id"),
                "realizationreport_id": item.get("realizationreport_id"),
                "date_from": item.get("date_from"),
                "date_to": item.get("date_to"),
                "create_dt": item.get("create_dt"),
                "supplier_name": item.get("supplier_name"),
                "nm_id": item.get("nm_id"),
                "brand_name": item.get("brand_name"),
                "sa_name": item.get("sa_name"),
                "ts_name": item.get("ts_name"),
                "barcode": item.get("barcode"),
                "subject_name": item.get("subject_name"),
                "doc_type_name": item.get("doc_type_name"),
                "quantity": item.get("quantity"),
                "retail_price": item.get("retail_price"),
                "retail_amount": item.get("retail_amount"),
                "sale_percent": item.get("sale_percent"),
                "commission_percent": item.get("commission_percent"),
                "office_name": item.get("office_name"),
                "supplier_oper_name": item.get("supplier_oper_name"),
                "order_dt": item.get("order_dt"),
                "sale_dt": item.get("sale_dt"),
                "rr_dt": item.get("rr_dt"),
                "retail_price_withdisc_rub": item.get("retail_price_withdisc_rub"),
                "delivery_amount": item.get("delivery_amount"),
                "return_amount": item.get("return_amount"),
                "delivery_rub": item.get("delivery_rub"),
                "ppvz_for_pay": item.get("ppvz_for_pay"),
                "ppvz_reward": item.get("ppvz_reward"),
                "ppvz_sales_commission": item.get("ppvz_sales_commission"),
                "ppvz_vw": item.get("ppvz_vw"),
                "ppvz_vw_nds": item.get("ppvz_vw_nds"),
                "acquiring_fee": item.get("acquiring_fee"),
                "penalty": item.get("penalty"),
                "additional_payment": item.get("additional_payment"),
                "storage_fee": item.get("storage_fee"),
                "deduction": item.get("deduction"),
                "acceptance": item.get("acceptance"),
                "rebill_logistic_cost": item.get("rebill_logistic_cost"),
                "site_country": item.get("site_country"),
                "srid": item.get("srid"),
                "gi_id": item.get("gi_id"),
                "rid": item.get("rid"),
                "kiz": item.get("kiz"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbFinancialReport).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["rrd_id"],
            set_={
                "realizationreport_id": stmt.excluded.realizationreport_id,
                "date_from": stmt.excluded.date_from,
                "date_to": stmt.excluded.date_to,
                "create_dt": stmt.excluded.create_dt,
                "supplier_name": stmt.excluded.supplier_name,
                "nm_id": stmt.excluded.nm_id,
                "brand_name": stmt.excluded.brand_name,
                "sa_name": stmt.excluded.sa_name,
                "ts_name": stmt.excluded.ts_name,
                "barcode": stmt.excluded.barcode,
                "subject_name": stmt.excluded.subject_name,
                "doc_type_name": stmt.excluded.doc_type_name,
                "quantity": stmt.excluded.quantity,
                "retail_price": stmt.excluded.retail_price,
                "retail_amount": stmt.excluded.retail_amount,
                "ppvz_for_pay": stmt.excluded.ppvz_for_pay,
                "delivery_rub": stmt.excluded.delivery_rub,
                "penalty": stmt.excluded.penalty,
                "additional_payment": stmt.excluded.additional_payment,
                "storage_fee": stmt.excluded.storage_fee,
                "deduction": stmt.excluded.deduction,
                "acceptance": stmt.excluded.acceptance,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 500, offset: int = 0) -> list[WbFinancialReport]:
        result = await self._session.execute(
            select(WbFinancialReport).order_by(WbFinancialReport.rrd_id.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(self, date_from: str | None = None, date_to: str | None = None, limit: int = 500, offset: int = 0) -> list[WbFinancialReport]:
        stmt = select(WbFinancialReport)
        if date_from:
            stmt = stmt.where(WbFinancialReport.sale_dt >= date_from)
        if date_to:
            stmt = stmt.where(WbFinancialReport.sale_dt <= date_to)
        stmt = stmt.order_by(WbFinancialReport.rrd_id.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
