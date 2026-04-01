"""
Контроллер WB: Аналитика WB (11)
WB API: seller-analytics-api.wildberries.ru
Tags: Воронка продаж (3), Аналитика продавца CSV (4), Поисковые запросы по вашим товарам (5), История остатков (4)
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.analytics.funnel import (
    FunnelGroupedHistoryRequest, FunnelHistoryRequest, FunnelProductsRequest,
)
from src.schemas.analytics.csv_report import NmReportDownloadRequest, NmReportRetryRequest
from src.schemas.analytics.search import (
    SearchGroupsRequest, SearchOrdersRequest, SearchReportRequest, SearchTextsRequest,
)
from src.schemas.analytics.stocks import (
    StocksGroupsRequest, StocksOfficesRequest, StocksProductsRequest, StocksSizesRequest,
)
from src.services.analytics.wb.analytics import AnalyticsWbService


class AnalyticsWbController(Controller):
    path = "/analytics"
    tags = ["11. API Wildberries"]

    # ── Воронка продаж ──────────────────────────────────────────────────────────

    @post(
        "/funnel/products",
        tags=["11. API Wildberries"],
        summary="Воронка продаж по товарам",
        description=(
            "Возвращает показатели воронки продаж (просмотры, корзины, заказы, выкупы) по артикулам.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/products`"
        ),
    )
    async def get_funnel_products(self, data: FunnelProductsRequest) -> dict:
        return await AnalyticsWbService().get_funnel_products(data)

    @post(
        "/funnel/products/history",
        tags=["11. API Wildberries"],
        summary="История воронки продаж по товарам",
        description=(
            "Возвращает динамику воронки продаж по артикулам за период.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/products/history`"
        ),
    )
    async def get_funnel_products_history(self, data: FunnelHistoryRequest) -> dict:
        return await AnalyticsWbService().get_funnel_products_history(data)

    @post(
        "/funnel/grouped/history",
        tags=["11. API Wildberries"],
        summary="Сгруппированная история воронки",
        description=(
            "Возвращает динамику воронки с группировкой по брендам, предметам или тегам.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/grouped/history`"
        ),
    )
    async def get_funnel_grouped_history(self, data: FunnelGroupedHistoryRequest) -> dict:
        return await AnalyticsWbService().get_funnel_grouped_history(data)

    # ── CSV-отчёты ──────────────────────────────────────────────────────────────

    @post(
        "/nm-report",
        tags=["11. API Wildberries"],
        summary="Создать задачу CSV-отчёта",
        description=(
            "Создаёт задачу на формирование CSV-отчёта по артикулам (аналитика продавца).\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads`"
        ),
    )
    async def create_nm_report(self, data: NmReportDownloadRequest) -> dict:
        return await AnalyticsWbService().create_nm_report(data)

    @get(
        "/nm-report",
        tags=["11. API Wildberries"],
        summary="Список задач CSV-отчётов",
        description=(
            "Возвращает список задач формирования CSV-отчётов с их статусами.\n\n"
            "**WB endpoint:** `GET seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads`"
        ),
    )
    async def get_nm_reports(
        self,
        download_ids: str | None = Parameter(
            None, query="filter[downloadIds]", description="Фильтр по ID задач через запятую."
        ),
    ) -> dict:
        return await AnalyticsWbService().get_nm_reports(download_ids)

    @post(
        "/nm-report/retry",
        tags=["11. API Wildberries"],
        summary="Повторить задачу CSV-отчёта",
        description=(
            "Повторно запускает задачу формирования CSV-отчёта.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads/retry`"
        ),
    )
    async def retry_nm_report(self, data: NmReportRetryRequest) -> dict:
        return await AnalyticsWbService().retry_nm_report(data)

    @get(
        "/nm-report/file/{download_id:str}",
        tags=["11. API Wildberries"],
        summary="Скачать CSV-отчёт",
        description=(
            "Скачивает готовый CSV-файл отчёта по артикулам.\n\n"
            "**WB endpoint:** `GET seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads/file/{downloadId}`"
        ),
    )
    async def get_nm_report_file(
        self,
        download_id: str = Parameter(description="ID задачи формирования отчёта"),
    ) -> dict:
        return await AnalyticsWbService().get_nm_report_file(download_id)

    # ── Поисковые запросы ───────────────────────────────────────────────────────

    @post(
        "/search/report",
        tags=["11. API Wildberries"],
        summary="Отчёт по поисковым запросам",
        description=(
            "Возвращает отчёт по поисковым запросам, через которые покупатели находили товары продавца.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/report`"
        ),
    )
    async def get_search_report(self, data: SearchReportRequest) -> dict:
        return await AnalyticsWbService().get_search_report(data)

    @post(
        "/search/groups",
        tags=["11. API Wildberries"],
        summary="Сгруппированные поисковые запросы",
        description=(
            "Возвращает сгруппированные поисковые запросы по категориям.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/table/groups`"
        ),
    )
    async def get_search_groups(self, data: SearchGroupsRequest) -> dict:
        return await AnalyticsWbService().get_search_groups(data)

    @post(
        "/search/details",
        tags=["11. API Wildberries"],
        summary="Детализация поисковых запросов",
        description=(
            "Возвращает детализированный список поисковых запросов.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/table/details`"
        ),
    )
    async def get_search_details(self, data: SearchReportRequest) -> dict:
        return await AnalyticsWbService().get_search_details(data)

    @post(
        "/search/texts",
        tags=["11. API Wildberries"],
        summary="Поисковые тексты по товару",
        description=(
            "Возвращает конкретные поисковые фразы, по которым нашли товар.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/product/search-texts`"
        ),
    )
    async def get_search_texts(self, data: SearchTextsRequest) -> dict:
        return await AnalyticsWbService().get_search_texts(data)

    @post(
        "/search/orders",
        tags=["11. API Wildberries"],
        summary="Заказы из поиска по товару",
        description=(
            "Возвращает данные о заказах из поиска по конкретному артикулу.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/product/orders`"
        ),
    )
    async def get_search_orders(self, data: SearchOrdersRequest) -> dict:
        return await AnalyticsWbService().get_search_orders(data)

    # ── История остатков ────────────────────────────────────────────────────────

    @post(
        "/stocks/groups",
        tags=["11. API Wildberries"],
        summary="История остатков по группам",
        description=(
            "Возвращает динамику остатков по группам товаров за период.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/groups`"
        ),
    )
    async def get_stocks_groups(self, data: StocksGroupsRequest) -> dict:
        return await AnalyticsWbService().get_stocks_groups(data)

    @post(
        "/stocks/products",
        tags=["11. API Wildberries"],
        summary="История остатков по артикулам",
        description=(
            "Возвращает динамику остатков по конкретным артикулам WB.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/products`"
        ),
    )
    async def get_stocks_products(self, data: StocksProductsRequest) -> dict:
        return await AnalyticsWbService().get_stocks_products(data)

    @post(
        "/stocks/sizes",
        tags=["11. API Wildberries"],
        summary="История остатков по размерам",
        description=(
            "Возвращает динамику остатков по размерам конкретного артикула.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/sizes`"
        ),
    )
    async def get_stocks_sizes(self, data: StocksSizesRequest) -> dict:
        return await AnalyticsWbService().get_stocks_sizes(data)

    @post(
        "/stocks/offices",
        tags=["11. API Wildberries"],
        summary="История остатков по складам",
        description=(
            "Возвращает динамику остатков в разбивке по складам WB.\n\n"
            "**WB endpoint:** `POST seller-analytics-api.wildberries.ru/api/v2/stocks-report/offices`"
        ),
    )
    async def get_stocks_offices(self, data: StocksOfficesRequest) -> dict:
        return await AnalyticsWbService().get_stocks_offices(data)
