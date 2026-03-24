"""
Контроллер WB: Отчёты WB (12)
WB API: statistics-api.wildberries.ru
Tags: Основные отчёты(3), Отчёт об остатках(3), Отчёты об удержаниях(5),
      Операции при приёмке(3), Платное хранение(3), Продажи по регионам(1),
      Доля бренда(3), Скрытые товары(2), Отчёт о возвратах(1), Маркировка(1)
Total: 25 endpoints
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.reports.main_reports import ExciseReportRequest
from src.services.reports.wb.reports import ReportsWbService


class ReportsWbController(Controller):
    path = "/reports"
    tags = ["WB / Отчёты"]

    # ── Основные отчёты ────────────────────────────────────────────────────────

    @get(
        "/stocks",
        tags=["Основные отчёты"],
        summary="Остатки на складах",
        description=(
            "Возвращает остатки товаров продавца на складах WB.\n\n"
            "Данные обновляются каждые 30 минут.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/supplier/stocks`"
        ),
    )
    async def get_stocks(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата обновления в формате `YYYY-MM-DDTHH:MM:SS`."),
    ) -> list:
        return await ReportsWbService().get_stocks(date_from)

    @get(
        "/orders",
        tags=["Основные отчёты"],
        summary="Заказы",
        description=(
            "Возвращает заказы за период. Данные обновляются каждые 30 минут.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/supplier/orders`"
        ),
    )
    async def get_orders(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DDTHH:MM:SS`."),
    ) -> list:
        return await ReportsWbService().get_orders(date_from)

    @get(
        "/sales",
        tags=["Основные отчёты"],
        summary="Продажи и возвраты",
        description=(
            "Возвращает продажи и возвраты за период. Данные обновляются каждые 30 минут.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/supplier/sales`"
        ),
    )
    async def get_sales(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DDTHH:MM:SS`."),
    ) -> list:
        return await ReportsWbService().get_sales(date_from)

    @post(
        "/excise",
        tags=["Отчёт о товарах c обязательной маркировкой"],
        summary="Отчёт по маркированным товарам",
        description=(
            "Возвращает отчёт о товарах с обязательной маркировкой за период.\n\n"
            "**WB endpoint:** `POST statistics-api.wildberries.ru/api/v1/analytics/excise-report`"
        ),
    )
    async def get_excise_report(self, data: ExciseReportRequest) -> dict:
        return await ReportsWbService().get_excise_report(data)

    # ── Остатки на складах (async task) ────────────────────────────────────────

    @get(
        "/warehouse-remains",
        tags=["Отчёт об остатках на складах"],
        summary="Создать задачу отчёта об остатках",
        description=(
            "Инициирует формирование отчёта об остатках на складах WB.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/warehouse_remains`"
        ),
    )
    async def create_warehouse_remains_task(
        self,
        locale: str | None = Parameter(None, query="locale", description="Язык ответа: `ru`, `en`."),
        group_by_brand: bool | None = Parameter(None, query="groupByBrand", description="Группировать по бренду."),
        group_by_subject: bool | None = Parameter(None, query="groupBySubject", description="Группировать по предмету."),
        group_by_sa: bool | None = Parameter(None, query="groupBySa", description="Группировать по артикулу продавца."),
        group_by_nm: bool | None = Parameter(None, query="groupByNm", description="Группировать по артикулу WB."),
        group_by_barcode: bool | None = Parameter(None, query="groupByBarcode", description="Группировать по баркоду."),
        group_by_size: bool | None = Parameter(None, query="groupBySize", description="Группировать по размеру."),
        filter_pics: bool | None = Parameter(None, query="filterPics", description="`true` — только с фото."),
        filter_volume: float | None = Parameter(None, query="filterVolume", description="Фильтр по объёму, л."),
    ) -> dict:
        params = {k: v for k, v in {
            "locale": locale, "groupByBrand": group_by_brand, "groupBySubject": group_by_subject,
            "groupBySa": group_by_sa, "groupByNm": group_by_nm, "groupByBarcode": group_by_barcode,
            "groupBySize": group_by_size, "filterPics": filter_pics, "filterVolume": filter_volume,
        }.items() if v is not None}
        return await ReportsWbService().create_warehouse_remains_task(params)

    @get(
        "/warehouse-remains/tasks/{task_id:str}/status",
        tags=["Отчёт об остатках на складах"],
        summary="Статус задачи отчёта об остатках",
        description=(
            "Возвращает статус задачи формирования отчёта об остатках.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/status`"
        ),
    )
    async def get_warehouse_remains_status(
        self,
        task_id: str = Parameter(description="ID задачи"),
    ) -> dict:
        return await ReportsWbService().get_warehouse_remains_status(task_id)

    @get(
        "/warehouse-remains/tasks/{task_id:str}/download",
        tags=["Отчёт об остатках на складах"],
        summary="Скачать отчёт об остатках",
        description=(
            "Скачивает готовый отчёт об остатках на складах.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/download`"
        ),
    )
    async def download_warehouse_remains(
        self,
        task_id: str = Parameter(description="ID задачи"),
    ) -> dict:
        return await ReportsWbService().download_warehouse_remains(task_id)

    # ── Удержания ──────────────────────────────────────────────────────────────

    @get(
        "/penalties/measurements",
        tags=["Отчёты об удержаниях"],
        summary="Штрафы за некорректные замеры",
        description=(
            "Возвращает список штрафов за некорректные замеры товаров на складе.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/analytics/v1/measurement-penalties`"
        ),
    )
    async def get_measurement_penalties(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания в формате `YYYY-MM-DD`."),
        limit: int = Parameter(100, query="limit", description="Количество записей. По умолчанию: 100."),
        offset: int = Parameter(0, query="offset", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await ReportsWbService().get_measurement_penalties(date_from, date_to, limit, offset)

    @get(
        "/measurements/warehouse",
        tags=["Отчёты об удержаниях"],
        summary="Данные обмеров на складе",
        description=(
            "Возвращает данные обмеров товаров на складе (измеренный vs. заявленный объём).\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/analytics/v1/warehouse-measurements`"
        ),
    )
    async def get_warehouse_measurements(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания в формате `YYYY-MM-DD`."),
        limit: int = Parameter(100, query="limit", description="Количество записей. По умолчанию: 100."),
        offset: int = Parameter(0, query="offset", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await ReportsWbService().get_warehouse_measurements(date_from, date_to, limit, offset)

    @get(
        "/deductions",
        tags=["Отчёты об удержаниях"],
        summary="Список удержаний",
        description=(
            "Возвращает список удержаний по рекламным и другим операциям.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/analytics/v1/deductions`"
        ),
    )
    async def get_deductions(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания в формате `YYYY-MM-DD`."),
        sort: str | None = Parameter(None, query="sort", description="Поле сортировки."),
        order: str | None = Parameter(None, query="order", description="`asc` или `desc`."),
        limit: int = Parameter(100, query="limit", description="Количество записей. По умолчанию: 100."),
        offset: int = Parameter(0, query="offset", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await ReportsWbService().get_deductions(date_from, date_to, sort, order, limit, offset)

    @get(
        "/antifraud",
        tags=["Отчёты об удержаниях"],
        summary="Детализация антифрод-удержаний",
        description=(
            "Возвращает детализацию удержаний по антифроду.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/antifraud-details`"
        ),
    )
    async def get_antifraud_details(self) -> dict:
        return await ReportsWbService().get_antifraud_details()

    @get(
        "/labeling",
        tags=["Отчёт о товарах c обязательной маркировкой"],
        summary="Товары с обязательной маркировкой",
        description=(
            "Возвращает список товаров продавца с обязательной маркировкой.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/goods-labeling`"
        ),
    )
    async def get_goods_labeling(self) -> dict:
        return await ReportsWbService().get_goods_labeling()

    # ── Операции при приёмке (async task) ─────────────────────────────────────

    @get(
        "/acceptance",
        tags=["Операции при приёмке"],
        summary="Создать задачу отчёта о приёмке",
        description=(
            "Инициирует формирование отчёта об операциях при приёмке товаров.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/acceptance_report`"
        ),
    )
    async def create_acceptance_report_task(self) -> dict:
        return await ReportsWbService().create_acceptance_report_task()

    @get(
        "/acceptance/tasks/{task_id:str}/status",
        tags=["Операции при приёмке"],
        summary="Статус задачи отчёта о приёмке",
        description=(
            "Возвращает статус задачи отчёта об операциях при приёмке.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/acceptance_report/tasks/{task_id}/status`"
        ),
    )
    async def get_acceptance_report_status(
        self,
        task_id: str = Parameter(description="ID задачи"),
    ) -> dict:
        return await ReportsWbService().get_acceptance_report_status(task_id)

    @get(
        "/acceptance/tasks/{task_id:str}/download",
        tags=["Операции при приёмке"],
        summary="Скачать отчёт о приёмке",
        description=(
            "Скачивает готовый отчёт об операциях при приёмке товаров.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/acceptance_report/tasks/{task_id}/download`"
        ),
    )
    async def download_acceptance_report(
        self,
        task_id: str = Parameter(description="ID задачи"),
    ) -> dict:
        return await ReportsWbService().download_acceptance_report(task_id)

    # ── Платное хранение (async task) ─────────────────────────────────────────

    @get(
        "/paid-storage",
        tags=["Платное хранение"],
        summary="Создать задачу отчёта о платном хранении",
        description=(
            "Инициирует формирование отчёта о стоимости платного хранения на складах WB.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/paid_storage`"
        ),
    )
    async def create_paid_storage_task(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания в формате `YYYY-MM-DD`."),
    ) -> dict:
        return await ReportsWbService().create_paid_storage_task(date_from, date_to)

    @get(
        "/paid-storage/tasks/{task_id:str}/status",
        tags=["Платное хранение"],
        summary="Статус задачи платного хранения",
        description=(
            "Возвращает статус задачи отчёта о платном хранении.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/paid_storage/tasks/{task_id}/status`"
        ),
    )
    async def get_paid_storage_status(
        self,
        task_id: str = Parameter(description="ID задачи"),
    ) -> dict:
        return await ReportsWbService().get_paid_storage_status(task_id)

    @get(
        "/paid-storage/tasks/{task_id:str}/download",
        tags=["Платное хранение"],
        summary="Скачать отчёт о платном хранении",
        description=(
            "Скачивает готовый отчёт о стоимости платного хранения.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/paid_storage/tasks/{task_id}/download`"
        ),
    )
    async def download_paid_storage(
        self,
        task_id: str = Parameter(description="ID задачи"),
    ) -> dict:
        return await ReportsWbService().download_paid_storage(task_id)

    # ── Продажи по регионам ────────────────────────────────────────────────────

    @get(
        "/region-sale",
        tags=["Продажи по регионам"],
        summary="Продажи по регионам",
        description=(
            "Возвращает статистику продаж в разбивке по регионам России.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/region-sale`"
        ),
    )
    async def get_region_sale(self) -> dict:
        return await ReportsWbService().get_region_sale()

    # ── Доля бренда ────────────────────────────────────────────────────────────

    @get(
        "/brand/brands",
        tags=["Доля бренда в продажах"],
        summary="Бренды продавца",
        description=(
            "Возвращает список брендов продавца для анализа доли в продажах.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/brand-share/brands`"
        ),
    )
    async def get_brand_brands(self) -> dict:
        return await ReportsWbService().get_brand_brands()

    @get(
        "/brand/parent-subjects",
        tags=["Доля бренда в продажах"],
        summary="Родительские категории для доли бренда",
        description=(
            "Возвращает список родительских категорий для анализа доли бренда.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/brand-share/parent-subjects`"
        ),
    )
    async def get_brand_parent_subjects(
        self,
        locale: str | None = Parameter(None, query="locale", description="Язык: `ru`, `en`."),
        brand: str | None = Parameter(None, query="brand", description="Название бренда."),
    ) -> dict:
        return await ReportsWbService().get_brand_parent_subjects(locale, brand)

    @get(
        "/brand/share",
        tags=["Доля бренда в продажах"],
        summary="Доля бренда в категории",
        description=(
            "Возвращает долю бренда в продажах по выбранной категории.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/brand-share`"
        ),
    )
    async def get_brand_share(
        self,
        parent_id: int = Parameter(query="parentId", description="ID родительской категории."),
        brand: str = Parameter(query="brand", description="Название бренда."),
    ) -> dict:
        return await ReportsWbService().get_brand_share(parent_id, brand)

    # ── Скрытые товары ─────────────────────────────────────────────────────────

    @get(
        "/hidden/blocked",
        tags=["Скрытые товары"],
        summary="Заблокированные товары",
        description=(
            "Возвращает список заблокированных (полностью скрытых) товаров продавца.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/banned-products/blocked`"
        ),
    )
    async def get_blocked_products(
        self,
        sort: str | None = Parameter(None, query="sort", description="Поле сортировки."),
        order: str | None = Parameter(None, query="order", description="`asc` или `desc`."),
    ) -> dict:
        return await ReportsWbService().get_blocked_products(sort, order)

    @get(
        "/hidden/shadowed",
        tags=["Скрытые товары"],
        summary="Частично скрытые товары",
        description=(
            "Возвращает список товаров, скрытых в некоторых категориях или регионах.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/banned-products/shadowed`"
        ),
    )
    async def get_shadowed_products(
        self,
        sort: str | None = Parameter(None, query="sort", description="Поле сортировки."),
        order: str | None = Parameter(None, query="order", description="`asc` или `desc`."),
    ) -> dict:
        return await ReportsWbService().get_shadowed_products(sort, order)

    # ── Возвраты ───────────────────────────────────────────────────────────────

    @get(
        "/returns",
        tags=["Отчёт о возвратах и перемещении товаров"],
        summary="Отчёт о возвратах товаров",
        description=(
            "Возвращает отчёт о возвратах и перемещении товаров за период.\n\n"
            "**WB endpoint:** `GET statistics-api.wildberries.ru/api/v1/analytics/goods-return`"
        ),
    )
    async def get_goods_return(
        self,
        date_from: str = Parameter(query="dateFrom", description="Дата начала в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="dateTo", description="Дата окончания в формате `YYYY-MM-DD`."),
    ) -> dict:
        return await ReportsWbService().get_goods_return(date_from, date_to)
