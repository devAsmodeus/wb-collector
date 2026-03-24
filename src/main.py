"""Точка входа — Litestar приложение."""
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.contrib.prometheus import PrometheusConfig, PrometheusController
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi.spec import Components, SecurityScheme, Tag
from litestar.di import Provide

from src.dependencies import provide_db_session, provide_db_manager
from src.exceptions import EXCEPTION_HANDLERS
from src.init import redis_manager
from src.logging_config import setup_logging
from src.middleware import RequestLoggingMiddleware

setup_logging(level="INFO")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(_: Litestar) -> AsyncGenerator[None, None]:
    await redis_manager.connect()
    logger.info("WB Collector started", extra={"event": "startup"})
    yield
    await redis_manager.close()
    logger.info("WB Collector stopped", extra={"event": "shutdown"})


# ---------------------------------------------------------------------------
# Системные роуты
# ---------------------------------------------------------------------------

@get("/health", tags=["System"], summary="Проверка работоспособности сервиса")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0"}


# ---------------------------------------------------------------------------
# Роутеры (подключаем по мере реализации)
# ---------------------------------------------------------------------------

from src.api.general import general_router
from src.api.products import products_router
from src.api.fbs import fbs_router
from src.api.dbw import dbw_router
from src.api.dbs import dbs_router
from src.api.pickup import pickup_router
from src.api.fbw import fbw_router
from src.api.promotion import promotion_router
from src.api.communications import communications_router
from src.api.tariffs import tariffs_router
from src.api.analytics import analytics_router
from src.api.reports import reports_router
from src.api.finances import finances_router

# ---------------------------------------------------------------------------
# Приложение
# ---------------------------------------------------------------------------

prometheus_config = PrometheusConfig(
    app_name="wb_collector",
    prefix="wb_collector_http",
    labels={"app": "wb-collector"},
)

app = Litestar(
    route_handlers=[
        health,
        PrometheusController,  # GET /metrics
        general_router,
        products_router,
        fbs_router,
        dbw_router,
        dbs_router,
        pickup_router,
        fbw_router,
        promotion_router,
        communications_router,
        tariffs_router,
        analytics_router,
        reports_router,
        finances_router,
    ],
    lifespan=[lifespan],
    dependencies={
        "db_session": Provide(provide_db_session),
        "db": Provide(provide_db_manager),
    },
    exception_handlers=EXCEPTION_HANDLERS,
    middleware=[prometheus_config.middleware, RequestLoggingMiddleware],
    openapi_config=OpenAPIConfig(
        title="WB Collector",
        version="0.1.0",
        description=(
            "Сбор и аналитика данных Wildberries API.\n\n"
            "**WB API** — прямые прокси к WB API с сохранением в БД.\n"
            "**Sync** — синхронизация данных в БД.\n"
            "**DB** — чтение данных из локальной БД.\n\n"
            "**Авторизация:** нажмите кнопку **Authorize** и введите WB API токен."
        ),
        components=Components(
            security_schemes={
                "BearerAuth": SecurityScheme(
                    type="http",
                    scheme="bearer",
                    bearer_format="JWT",
                    description="WB API токен. Формат: Bearer <token>",
                )
            }
        ),
        security=[{"BearerAuth": []}],
        render_plugins=[SwaggerRenderPlugin(version="5.18.2", js_url=None, css_url=None)],
        path="/docs",
        tags=[
            Tag(name="System", description="Служебные эндпоинты"),
            Tag(name="WB / General", description="Прокси к WB API / Общее (01)"),
            Tag(name="Sync / General", description="Синхронизация в БД / Общее (01)"),
            Tag(name="DB / General", description="Данные из БД / Общее (01)"),
            Tag(name="General — Пользователи", description="WB API / Общее / Управление пользователями"),
            Tag(name="Products — Справочники", description="WB API / Товары / Справочники"),
            Tag(name="Products — Теги", description="WB API / Товары / Теги"),
            Tag(name="Products — Карточки", description="WB API / Товары / Карточки"),
            Tag(name="Products — Цены", description="WB API / Товары / Цены и скидки"),
            Tag(name="Products — Склады", description="WB API / Товары / Остатки и склады"),
            Tag(name="Пропуска FBS", description="WB API / Заказы FBS / Пропуска на склады WB"),
            Tag(name="Сборочные задания FBS", description="WB API / Заказы FBS / Сборочные задания"),
            Tag(name="Метаданные FBS", description="WB API / Заказы FBS / Метаданные сборочных заданий"),
            Tag(name="Поставки FBS", description="WB API / Заказы FBS / Поставки и короба"),
            Tag(name="Сборочные задания DBW", description="WB API / Заказы DBW / Сборочные задания"),
            Tag(name="Метаданные DBW", description="WB API / Заказы DBW / Метаданные сборочных заданий"),
            Tag(name="Сборочные задания DBS", description="WB API / Заказы DBS / Сборочные задания"),
            Tag(name="Метаданные DBS", description="WB API / Заказы DBS / Метаданные сборочных заданий"),
            Tag(name="Сборочные задания Самовывоз", description="WB API / Самовывоз / Сборочные задания"),
            Tag(name="Метаданные Самовывоз", description="WB API / Самовывоз / Метаданные сборочных заданий"),
            Tag(name="Информация для формирования поставок", description="WB API / Поставки FBW / Опции приёмки, склады, тарифы"),
            Tag(name="Информация о поставках", description="WB API / Поставки FBW / Список и детали поставок"),
            Tag(name="Кампании", description="WB API / Маркетинг / Рекламные кампании"),
            Tag(name="Управление кампаниями", description="WB API / Маркетинг / Управление кампаниями"),
            Tag(name="Создание кампаний", description="WB API / Маркетинг / Создание кампаний"),
            Tag(name="Финансы", description="WB API / Маркетинг / Финансы и бюджет"),
            Tag(name="Поисковые кластеры", description="WB API / Маркетинг / Поисковые кластеры"),
            Tag(name="Статистика", description="WB API / Маркетинг / Статистика кампаний"),
            Tag(name="Медиа", description="WB API / Маркетинг / Медиакампании"),
            Tag(name="Календарь акций", description="WB API / Маркетинг / Календарь промоакций WB"),
            Tag(name="Вопросы", description="WB API / Коммуникации / Вопросы покупателей"),
            Tag(name="Отзывы", description="WB API / Коммуникации / Отзывы покупателей"),
            Tag(name="Закреплённые отзывы", description="WB API / Коммуникации / Закреплённые отзывы"),
            Tag(name="Чат с покупателями", description="WB API / Коммуникации / Чат с покупателями"),
            Tag(name="Возвраты покупателями", description="WB API / Коммуникации / Возвраты по отзывам"),
            Tag(name="Тарифы", description="WB API / Тарифы WB / Общие тарифы"),
            Tag(name="Комиссии", description="WB API / Тарифы WB / Комиссии по категориям"),
            Tag(name="Стоимость возврата продавцу", description="WB API / Тарифы WB / Возврат со складов WB"),
            Tag(name="Тарифы на остаток", description="WB API / Тарифы WB / Хранение и доставка"),
            Tag(name="Тарифы на поставку", description="WB API / Тарифы WB / Коэффициенты складов"),
            Tag(name="Аналитика", description="WB API / Аналитика / Общая аналитика продавца"),
            Tag(name="Воронка продаж", description="WB API / Аналитика / Воронка продаж"),
            Tag(name="Аналитика продавца CSV", description="WB API / Аналитика / CSV-отчёты"),
            Tag(name="Поисковые запросы по вашим товарам", description="WB API / Аналитика / Поисковые запросы"),
            Tag(name="История остатков", description="WB API / Аналитика / История остатков"),
            Tag(name="Отчёты", description="WB API / Отчёты / Общие отчёты"),
            Tag(name="Основные отчёты", description="WB API / Отчёты / Остатки, заказы, продажи"),
            Tag(name="Отчёт об остатках на складах", description="WB API / Отчёты / Остатки на складах WB"),
            Tag(name="Отчёты об удержаниях", description="WB API / Отчёты / Удержания, штрафы, обмеры"),
            Tag(name="Операции при приёмке", description="WB API / Отчёты / Приёмка товаров"),
            Tag(name="Платное хранение", description="WB API / Отчёты / Платное хранение на складах WB"),
            Tag(name="Продажи по регионам", description="WB API / Отчёты / Региональные продажи"),
            Tag(name="Доля бренда в продажах", description="WB API / Отчёты / Доля бренда"),
            Tag(name="Скрытые товары", description="WB API / Отчёты / Заблокированные и скрытые товары"),
            Tag(name="Отчёт о возвратах и перемещении товаров", description="WB API / Отчёты / Возвраты"),
            Tag(name="Отчёт о товарах c обязательной маркировкой", description="WB API / Отчёты / Маркировка"),
            Tag(name="Финансы WB", description="WB API / Финансы / Баланс, отчёты, документы"),
            Tag(name="Баланс", description="WB API / Финансы / Баланс продавца"),
            Tag(name="Финансовые отчёты", description="WB API / Финансы / Детальный финансовый отчёт"),
            Tag(name="Документы", description="WB API / Финансы / Документы продавца"),
            Tag(name="Sync / Products", description="Синхронизация в БД / Товары (02)"),
            Tag(name="DB / Products", description="Данные из БД / Товары (02)"),
            Tag(name="Sync / FBS", description="Синхронизация в БД / Заказы FBS (03)"),
            Tag(name="DB / FBS", description="Данные из БД / Заказы FBS (03)"),
            Tag(name="Sync / DBW", description="Синхронизация в БД / Заказы DBW (04)"),
            Tag(name="DB / DBW", description="Данные из БД / Заказы DBW (04)"),
            Tag(name="Sync / DBS", description="Синхронизация в БД / Заказы DBS (05)"),
            Tag(name="DB / DBS", description="Данные из БД / Заказы DBS (05)"),
            Tag(name="Sync / Pickup", description="Синхронизация в БД / Самовывоз (06)"),
            Tag(name="DB / Pickup", description="Данные из БД / Самовывоз (06)"),
            Tag(name="Sync / Promotion", description="Синхронизация в БД / Маркетинг (08)"),
            Tag(name="DB / Promotion", description="Данные из БД / Маркетинг (08)"),
            Tag(name="Sync / Communications", description="Синхронизация в БД / Коммуникации (09)"),
            Tag(name="DB / Communications", description="Данные из БД / Коммуникации (09)"),
            Tag(name="Sync / Tariffs", description="Синхронизация в БД / Тарифы (10)"),
            Tag(name="DB / Tariffs", description="Данные из БД / Тарифы (10)"),
            Tag(name="Sync / Reports", description="Синхронизация в БД / Отчёты (12)"),
            Tag(name="DB / Reports", description="Данные из БД / Отчёты (12)"),
            Tag(name="Sync / Finances", description="Синхронизация в БД / Финансы (13)"),
            Tag(name="DB / Finances", description="Данные из БД / Финансы (13)"),
            Tag(name="Internal", description="Кастомные методы — агрегация, экспорт, аналитика"),
        ],
    ),
    cors_config=CORSConfig(allow_origins=["*"]),
)
