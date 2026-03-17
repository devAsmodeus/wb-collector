"""Точка входа — Litestar приложение."""
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.contrib.prometheus import PrometheusConfig, PrometheusController
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Tag
from litestar.di import Provide

from src.dependencies import provide_db_session, provide_db_manager
from src.exceptions import EXCEPTION_HANDLERS
from src.init import redis_manager
from src.logging_config import setup_logging

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
    ],
    lifespan=[lifespan],
    dependencies={
        "db_session": Provide(provide_db_session),
        "db": Provide(provide_db_manager),
    },
    exception_handlers=EXCEPTION_HANDLERS,
    middleware=[prometheus_config.middleware],
    openapi_config=OpenAPIConfig(
        title="WB Collector",
        version="0.1.0",
        description=(
            "Сбор и аналитика данных Wildberries API.\n\n"
            "**WB API** — прямые прокси к WB API с сохранением в БД.\n"
            "**Internal** — кастомная логика, агрегация, экспорт."
        ),
        tags=[
            Tag(name="System", description="Служебные эндпоинты"),
            Tag(name="General — Продавец", description="WB API / Общее / Информация о продавце"),
            Tag(name="General — Новости", description="WB API / Общее / Новости"),
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
            Tag(name="Internal", description="Кастомные методы — агрегация, экспорт, аналитика"),
        ],
        path="/docs",
    ),
    cors_config=CORSConfig(allow_origins=["*"]),
)
