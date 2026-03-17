"""Сервис: Финансы WB."""
from src.collectors.finances.finances import FinancesCollector
from src.schemas.finances.finances import DownloadAllDocumentsRequest
from src.services.base import BaseService


class FinancesService(BaseService):
    async def get_balance(self) -> dict:
        async with FinancesCollector() as c: return await c.get_balance()

    async def get_financial_report(self, date_from, date_to, limit=100000, rrdid=0, period=None) -> list:
        async with FinancesCollector() as c: return await c.get_financial_report(date_from, date_to, limit, rrdid, period)

    async def get_document_categories(self) -> dict:
        async with FinancesCollector() as c: return await c.get_document_categories()

    async def get_documents(self, begin_time=None, end_time=None, sort=None, order=None, category=None, service_name=None, limit=100, offset=0) -> dict:
        async with FinancesCollector() as c:
            return await c.get_documents(begin_time, end_time, sort, order, category, service_name, limit, offset)

    async def download_document(self, service_name: str, extension: str) -> dict:
        async with FinancesCollector() as c: return await c.download_document(service_name, extension)

    async def download_all_documents(self, data: DownloadAllDocumentsRequest) -> dict:
        async with FinancesCollector() as c: return await c.download_all_documents(data.model_dump(exclude_none=True))
