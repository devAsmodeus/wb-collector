"""Точка входа — Litestar приложение."""
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.contrib.prometheus import PrometheusConfig, PrometheusController
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme, Tag

from src.plugins.scalar import ScalarRenderPlugin
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
            "**WB** — прямые прокси-запросы к WB API.\n"
            "**Sync** — синхронизация данных WB API → PostgreSQL.\n"
            "**DB** — чтение данных из локальной БД.\n\n"
            "Авторизация: нажмите **Authorize** и введите WB API токен."
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
        render_plugins=[ScalarRenderPlugin()],
        path="/docs",
        tags=[
            # Система
            Tag(name="System", description="Проверка работоспособности сервиса"),
            # 01. Общие
            Tag(name="01. API Wildberries", description="Прямые запросы к WB API: проверка связи, информация о продавце, новости"),
            Tag(name="01. Синхронизация", description="Загрузка общих данных (продавец, новости) из WB API в PostgreSQL"),
            Tag(name="01. База данных", description="Получение общих данных (продавец, новости) из локальной БД"),
            # 02. Товары
            Tag(name="02. API Wildberries", description="Прямые запросы к WB API: карточки, цены, справочники, склады, теги, медиа"),
            Tag(name="02. Синхронизация", description="Загрузка товаров, цен, справочников и складов из WB API в PostgreSQL"),
            Tag(name="02. База данных", description="Получение товаров, цен, справочников и складов из локальной БД"),
            # 03. FBS
            Tag(name="03. API Wildberries", description="Прямые запросы к WB API: заказы, поставки, пропуска, мета-данные FBS"),
            Tag(name="03. Синхронизация", description="Загрузка заказов FBS из WB API в PostgreSQL"),
            Tag(name="03. База данных", description="Получение заказов FBS из локальной БД"),
            # 04. DBW (Доставка на склад WB)
            Tag(name="04. API Wildberries", description="Прямые запросы к WB API: заказы и мета-данные DBW"),
            Tag(name="04. Синхронизация", description="Загрузка заказов DBW из WB API в PostgreSQL"),
            Tag(name="04. База данных", description="Получение заказов DBW из локальной БД"),
            # 05. DBS (Доставка силами продавца)
            Tag(name="05. API Wildberries", description="Прямые запросы к WB API: заказы и мета-данные DBS"),
            Tag(name="05. Синхронизация", description="Загрузка заказов DBS из WB API в PostgreSQL"),
            Tag(name="05. База данных", description="Получение заказов DBS из локальной БД"),
            # 06. Самовывоз
            Tag(name="06. API Wildberries", description="Прямые запросы к WB API: заказы самовывоза, мета-данные ПВЗ"),
            Tag(name="06. Синхронизация", description="Загрузка заказов самовывоза из WB API в PostgreSQL"),
            Tag(name="06. База данных", description="Получение заказов самовывоза из локальной БД"),
            # 07. FBW (Склады WB)
            Tag(name="07. API Wildberries", description="Прямые запросы к WB API: поставки и приёмка на склады FBW"),
            # 08. Продвижение
            Tag(name="08. API Wildberries", description="Прямые запросы к WB API: рекламные кампании, ставки, статистика, акции, финансы продвижения"),
            Tag(name="08. Синхронизация", description="Загрузка рекламных кампаний и акций из WB API в PostgreSQL"),
            Tag(name="08. База данных", description="Получение рекламных кампаний и акций из локальной БД"),
            # 09. Коммуникации
            Tag(name="09. API Wildberries", description="Прямые запросы к WB API: чаты, отзывы, вопросы, претензии, закрепы"),
            Tag(name="09. Синхронизация", description="Загрузка отзывов, вопросов и претензий из WB API в PostgreSQL"),
            Tag(name="09. База данных", description="Получение отзывов, вопросов и претензий из локальной БД"),
            # 10. Тарифы
            Tag(name="10. API Wildberries", description="Прямые запросы к WB API: комиссии, тарифы коробов, паллетов, поставок"),
            Tag(name="10. Синхронизация", description="Загрузка тарифов и комиссий из WB API в PostgreSQL"),
            Tag(name="10. База данных", description="Получение тарифов и комиссий из локальной БД"),
            # 11. Аналитика
            Tag(name="11. API Wildberries", description="Прямые запросы к WB API: воронка продаж, отчёты по артикулам, аналитика поиска, остатки"),
            # 12. Отчёты
            Tag(name="12. API Wildberries", description="Прямые запросы к WB API: остатки, заказы, продажи, акцизы, хранение, штрафы, возвраты, антифрод"),
            Tag(name="12. Синхронизация", description="Загрузка отчётов (остатки, заказы, продажи) из WB API в PostgreSQL"),
            Tag(name="12. База данных", description="Получение отчётов (остатки, заказы, продажи) из локальной БД"),
            # 13. Финансы
            Tag(name="13. API Wildberries", description="Прямые запросы к WB API: баланс, финансовый отчёт, документы"),
            Tag(name="13. Синхронизация", description="Загрузка финансовых отчётов из WB API в PostgreSQL"),
            Tag(name="13. База данных", description="Получение финансовых отчётов из локальной БД"),
        ],
    ),
    cors_config=CORSConfig(allow_origins=["*"]),
)
