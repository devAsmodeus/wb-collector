"""Сервис WB: Отчёты WB."""
from src.collectors.reports.reports import ReportsCollector
from src.schemas.reports.main_reports import ExciseReportRequest
from src.services.base import BaseService


class ReportsWbService(BaseService):
    async def get_stocks(self, date_from: str) -> list:
        async with ReportsCollector() as c: return await c.get_stocks(date_from)

    async def get_orders(self, date_from: str) -> list:
        async with ReportsCollector() as c: return await c.get_orders(date_from)

    async def get_sales(self, date_from: str) -> list:
        async with ReportsCollector() as c: return await c.get_sales(date_from)

    async def get_excise_report(self, data: ExciseReportRequest) -> dict:
        async with ReportsCollector() as c: return await c.get_excise_report(data.model_dump())

    async def create_warehouse_remains_task(self, params: dict) -> dict:
        async with ReportsCollector() as c: return await c.create_warehouse_remains_task(params)

    async def get_warehouse_remains_status(self, task_id: str) -> dict:
        async with ReportsCollector() as c: return await c.get_warehouse_remains_status(task_id)

    async def download_warehouse_remains(self, task_id: str) -> dict:
        async with ReportsCollector() as c: return await c.download_warehouse_remains(task_id)

    async def get_measurement_penalties(self, date_from, date_to, limit=100, offset=0) -> dict:
        async with ReportsCollector() as c: return await c.get_measurement_penalties(date_from, date_to, limit, offset)

    async def get_warehouse_measurements(self, date_from, date_to, limit=100, offset=0) -> dict:
        async with ReportsCollector() as c: return await c.get_warehouse_measurements(date_from, date_to, limit, offset)

    async def get_deductions(self, date_from, date_to, sort=None, order=None, limit=100, offset=0) -> dict:
        async with ReportsCollector() as c: return await c.get_deductions(date_from, date_to, sort, order, limit, offset)

    async def get_antifraud_details(self) -> dict:
        async with ReportsCollector() as c: return await c.get_antifraud_details()

    async def get_goods_labeling(self) -> dict:
        async with ReportsCollector() as c: return await c.get_goods_labeling()

    async def create_acceptance_report_task(self) -> dict:
        async with ReportsCollector() as c: return await c.create_acceptance_report_task()

    async def get_acceptance_report_status(self, task_id: str) -> dict:
        async with ReportsCollector() as c: return await c.get_acceptance_report_status(task_id)

    async def download_acceptance_report(self, task_id: str) -> dict:
        async with ReportsCollector() as c: return await c.download_acceptance_report(task_id)

    async def create_paid_storage_task(self, date_from, date_to) -> dict:
        async with ReportsCollector() as c: return await c.create_paid_storage_task(date_from, date_to)

    async def get_paid_storage_status(self, task_id: str) -> dict:
        async with ReportsCollector() as c: return await c.get_paid_storage_status(task_id)

    async def download_paid_storage(self, task_id: str) -> dict:
        async with ReportsCollector() as c: return await c.download_paid_storage(task_id)

    async def get_region_sale(self) -> dict:
        async with ReportsCollector() as c: return await c.get_region_sale()

    async def get_brand_brands(self) -> dict:
        async with ReportsCollector() as c: return await c.get_brand_brands()

    async def get_brand_parent_subjects(self, locale=None, brand=None) -> dict:
        async with ReportsCollector() as c: return await c.get_brand_parent_subjects(locale, brand)

    async def get_brand_share(self, parent_id: int, brand: str) -> dict:
        async with ReportsCollector() as c: return await c.get_brand_share(parent_id, brand)

    async def get_blocked_products(self, sort=None, order=None) -> dict:
        async with ReportsCollector() as c: return await c.get_blocked_products(sort, order)

    async def get_shadowed_products(self, sort=None, order=None) -> dict:
        async with ReportsCollector() as c: return await c.get_shadowed_products(sort, order)

    async def get_goods_return(self, date_from, date_to) -> dict:
        async with ReportsCollector() as c: return await c.get_goods_return(date_from, date_to)
