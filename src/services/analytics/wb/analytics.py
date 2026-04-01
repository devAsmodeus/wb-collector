"""Сервис WB: Аналитика WB."""
from src.collectors.analytics.analytics import AnalyticsCollector
from src.schemas.analytics.funnel import FunnelProductsRequest, FunnelHistoryRequest, FunnelGroupedHistoryRequest
from src.schemas.analytics.csv_report import NmReportDownloadRequest, NmReportRetryRequest
from src.schemas.analytics.search import SearchReportRequest, SearchGroupsRequest, SearchTextsRequest, SearchOrdersRequest
from src.schemas.analytics.stocks import StocksGroupsRequest, StocksProductsRequest, StocksSizesRequest, StocksOfficesRequest
from src.services.base import BaseService


class AnalyticsWbService(BaseService):
    async def get_funnel_products(self, data: FunnelProductsRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_funnel_products(data.model_dump(exclude_none=True))

    async def get_funnel_products_history(self, data: FunnelHistoryRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_funnel_products_history(data.model_dump(exclude_none=True))

    async def get_funnel_grouped_history(self, data: FunnelGroupedHistoryRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_funnel_grouped_history(data.model_dump(exclude_none=True))

    async def create_nm_report(self, data: NmReportDownloadRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.create_nm_report(data.model_dump(exclude_none=True))

    async def get_nm_reports(self, download_ids=None) -> dict:
        async with AnalyticsCollector() as c: return await c.get_nm_reports(download_ids)

    async def retry_nm_report(self, data: NmReportRetryRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.retry_nm_report(data.model_dump())

    async def get_nm_report_file(self, download_id: str) -> dict:
        async with AnalyticsCollector() as c: return await c.get_nm_report_file(download_id)

    async def get_search_report(self, data: SearchReportRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_search_report(data.model_dump(exclude_none=True))

    async def get_search_groups(self, data: SearchGroupsRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_search_groups(data.model_dump(exclude_none=True))

    async def get_search_details(self, data: SearchReportRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_search_details(data.model_dump(exclude_none=True))

    async def get_search_texts(self, data: SearchTextsRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_search_texts(data.model_dump(exclude_none=True))

    async def get_search_orders(self, data: SearchOrdersRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_search_orders(data.model_dump(exclude_none=True))

    async def get_stocks_groups(self, data: StocksGroupsRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_stocks_groups(data.model_dump(exclude_none=True))

    async def get_stocks_products(self, data: StocksProductsRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_stocks_products(data.model_dump(exclude_none=True))

    async def get_stocks_sizes(self, data: StocksSizesRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_stocks_sizes(data.model_dump(exclude_none=True))

    async def get_stocks_offices(self, data: StocksOfficesRequest) -> dict:
        async with AnalyticsCollector() as c: return await c.get_stocks_offices(data.model_dump(exclude_none=True))
