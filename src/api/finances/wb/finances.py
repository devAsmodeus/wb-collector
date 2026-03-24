"""
Контроллер WB: Финансы WB (13)
WB API: seller-api.wildberries.ru / finances-api.wildberries.ru
Tags: Баланс(1), Финансовые отчёты(1), Документы(4)
Total: 6 endpoints
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.finances.finances import DownloadAllDocumentsRequest
from src.services.finances.wb.finances import FinancesWbService


class FinancesWbController(Controller):
    path = "/finances"
    tags = ["WB / Финансы"]

    @get(
        "/balance",
        tags=["Баланс"],
        summary="Баланс продавца",
        description=(
            "Возвращает текущий баланс продавца на счёте WB.\n\n"
            "**WB endpoint:** `GET seller-api.wildberries.ru/api/v1/account/balance`"
        ),
    )
    async def get_balance(self) -> dict:
        return await FinancesWbService().get_balance()

    @get(
        "/report",
        tags=["Финансовые отчёты"],
        summary="Детальный финансовый отчёт",
        description=(
            "Возвращает детальный отчёт о реализации товаров за период (аналог отчёта продавца в ЛК WB).\n\n"
            "Параметр `rrdid` используется для постраничной загрузки — передайте последний `rrd_id` из предыдущего ответа.\n\n"
            "**WB endpoint:** `GET seller-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod`"
        ),
    )
    async def get_financial_report(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала периода в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания периода в формате `YYYY-MM-DD`."),
        limit: int = Parameter(100000, query="limit", description="Количество строк. Максимум: 100000."),
        rrdid: int = Parameter(0, query="rrdid", description="ID последней записи предыдущей страницы (для пагинации). По умолчанию: 0."),
        period: int | None = Parameter(None, query="period", description="Номер недели: `1`-я или `2`-я."),
    ) -> list:
        return await FinancesWbService().get_financial_report(date_from, date_to, limit, rrdid, period)

    @get(
        "/documents/categories",
        tags=["Документы"],
        summary="Категории документов",
        description=(
            "Возвращает список доступных категорий документов продавца.\n\n"
            "**WB endpoint:** `GET seller-api.wildberries.ru/api/v1/documents/categories`"
        ),
    )
    async def get_document_categories(self) -> dict:
        return await FinancesWbService().get_document_categories()

    @get(
        "/documents",
        tags=["Документы"],
        summary="Список документов",
        description=(
            "Возвращает список документов продавца с фильтрацией по дате, категории и сервису.\n\n"
            "**WB endpoint:** `GET seller-api.wildberries.ru/api/v1/documents/list`"
        ),
    )
    async def get_documents(
        self,
        begin_time: str | None = Parameter(None, query="beginTime", description="Начало периода (ISO 8601)."),
        end_time: str | None = Parameter(None, query="endTime", description="Конец периода (ISO 8601)."),
        sort: str | None = Parameter(None, query="sort", description="Поле сортировки."),
        order: str | None = Parameter(None, query="order", description="`asc` или `desc`."),
        category: str | None = Parameter(None, query="category", description="Категория документов."),
        service_name: str | None = Parameter(None, query="serviceName", description="Название сервиса."),
        limit: int = Parameter(100, query="limit", description="Количество записей. По умолчанию: 100."),
        offset: int = Parameter(0, query="offset", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await FinancesWbService().get_documents(begin_time, end_time, sort, order, category, service_name, limit, offset)

    @get(
        "/documents/download",
        tags=["Документы"],
        summary="Скачать документ",
        description=(
            "Скачивает конкретный документ по названию сервиса и формату.\n\n"
            "**WB endpoint:** `GET seller-api.wildberries.ru/api/v1/documents/download`"
        ),
    )
    async def download_document(
        self,
        service_name: str = Parameter(query="serviceName", description="Название сервиса документа."),
        extension: str = Parameter(query="extension", description="Формат файла: `pdf` или `xlsx`."),
    ) -> dict:
        return await FinancesWbService().download_document(service_name, extension)

    @post(
        "/documents/download/all",
        tags=["Документы"],
        summary="Скачать все документы",
        description=(
            "Скачивает все документы по указанным сервисам и формату.\n\n"
            "**WB endpoint:** `POST seller-api.wildberries.ru/api/v1/documents/download/all`"
        ),
    )
    async def download_all_documents(self, data: DownloadAllDocumentsRequest) -> dict:
        return await FinancesWbService().download_all_documents(data)
