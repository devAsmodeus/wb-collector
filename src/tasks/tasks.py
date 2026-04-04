"""Celery-задачи синхронизации данных WB API → БД.

Правило: 1 задача = 1 sync-эндпоинт. Всего 25 задач = 25 эндпоинтов.

Каждая задача:
1. Создаёт async event loop (Celery работает синхронно)
2. Вызывает sync-сервис, который забирает данные из WB API и кладёт в БД
3. Логирует результат
4. При ошибке — retry с фиксированной паузой 60 секунд (макс 3 попытки)
"""
import asyncio
import logging
from src.tasks.celery_app import celery_app
from src.utils.db_manager import DBManager

logger = logging.getLogger(__name__)


def run_async(coro):
    """Запускает корутину в синхронном контексте Celery (ForkPoolWorker)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        try:
            loop.run_until_complete(loop.shutdown_asyncgens())
        except Exception:
            pass
        loop.close()
        asyncio.set_event_loop(None)


# ---------------------------------------------------------------------------
# (01) General — Продавец и Новости
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.general.seller_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_general_seller_full(self):
    """POST /general/sync/seller/full — полная синхронизация продавца."""
    from src.services.general.sync.seller import SellerSyncService

    async def _run():
        async with DBManager() as db:
            result = await SellerSyncService().sync_seller_full(db.session)
        logger.info(f"[sync.general.seller_full] Done")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.general.news_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_general_news_full(self):
    """POST /general/sync/news/full — полная синхронизация новостей."""
    from src.services.general.sync.news import NewsSyncService

    async def _run():
        async with DBManager() as db:
            result = await NewsSyncService().sync_news_full(db.session)
        logger.info(f"[sync.general.news_full] Synced: {result.get('synced', 0)} news")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.general.news_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_general_news_incremental(self):
    """POST /general/sync/news/incremental — инкрементальная синхронизация новостей."""
    from src.services.general.sync.news import NewsSyncService

    async def _run():
        async with DBManager() as db:
            result = await NewsSyncService().sync_news_incremental(db.session)
        logger.info(f"[sync.general.news_incremental] Synced: {result.get('synced', 0)} news")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (02) Products — Карточки, цены, теги, склады, справочники
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.products.cards_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_products_cards_full(self):
    """POST /products/sync/cards/full — полная синхронизация карточек."""
    from src.services.products.sync.cards import CardsSyncService

    async def _run():
        async with DBManager() as db:
            result = await CardsSyncService().sync_cards_full(db.session)
        logger.info(f"[sync.products.cards_full] Synced: {result.get('synced', 0)} cards")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.products.prices_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_products_prices_full(self):
    """POST /products/sync/prices/full — полная синхронизация цен."""
    from src.services.products.sync.prices import PricesSyncService

    async def _run():
        async with DBManager() as db:
            result = await PricesSyncService().sync_prices_full(db.session)
        logger.info(f"[sync.products.prices_full] Synced: {result.get('synced', 0)} prices")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.products.tags_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_products_tags_full(self):
    """POST /products/sync/tags/full — полная синхронизация тегов."""
    from src.services.products.sync.tags import TagsSyncService

    async def _run():
        async with DBManager() as db:
            result = await TagsSyncService().sync_tags_full(db.session)
        logger.info(f"[sync.products.tags_full] Synced: {result.get('synced', 0)} tags")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.products.warehouses_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_products_warehouses_full(self):
    """POST /products/sync/warehouses/full — полная синхронизация складов."""
    from src.services.products.sync.warehouses import WarehousesSyncService

    async def _run():
        async with DBManager() as db:
            result = await WarehousesSyncService().sync_warehouses_full(db.session)
        logger.info(f"[sync.products.warehouses_full] Synced: {result.get('synced', 0)} warehouses")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.products.directories_categories",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_products_directories_categories(self):
    """POST /products/sync/directories/categories — синхронизация категорий."""
    from src.services.products.sync.directories import DirectoriesSyncService

    async def _run():
        async with DBManager() as db:
            result = await DirectoriesSyncService().sync_categories(db.session)
        logger.info(f"[sync.products.directories_categories] Synced: {result.get('synced', 0)} categories")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.products.directories_subjects",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_products_directories_subjects(self):
    """POST /products/sync/directories/subjects — синхронизация предметов."""
    from src.services.products.sync.directories import DirectoriesSyncService

    async def _run():
        async with DBManager() as db:
            result = await DirectoriesSyncService().sync_subjects(db.session)
        logger.info(f"[sync.products.directories_subjects] Synced: {result.get('synced', 0)} subjects")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (03) FBS — Заказы
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.fbs.orders_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_orders_full(self):
    """POST /fbs/sync/orders/full — полная синхронизация заказов FBS."""
    from src.services.fbs.sync.orders import FbsOrdersSyncService

    async def _run():
        async with DBManager() as db:
            result = await FbsOrdersSyncService().sync_orders(db.session)
        logger.info(f"[sync.fbs.orders_full] Synced: {result.get('synced', 0)} orders")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (04) DBW — Заказы
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.dbw.orders_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_dbw_orders_full(self):
    """POST /dbw/sync/orders/full — полная синхронизация заказов DBW."""
    from src.services.dbw.sync.orders import DbwOrdersSyncService

    async def _run():
        async with DBManager() as db:
            result = await DbwOrdersSyncService().sync_orders_full(db.session)
        logger.info(f"[sync.dbw.orders_full] Synced: {result.get('synced', 0)} orders")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (05) DBS — Заказы
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.dbs.orders_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_dbs_orders_full(self):
    """POST /dbs/sync/orders/full — полная синхронизация заказов DBS."""
    from src.services.dbs.sync.orders import DbsOrdersSyncService

    async def _run():
        async with DBManager() as db:
            result = await DbsOrdersSyncService().sync_orders_full(db.session)
        logger.info(f"[sync.dbs.orders_full] Synced: {result.get('synced', 0)} orders")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (06) Pickup — Заказы
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.pickup.orders_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_pickup_orders_full(self):
    """POST /pickup/sync/orders/full — полная синхронизация заказов Самовывоз."""
    from src.services.pickup.sync.orders import PickupOrdersSyncService

    async def _run():
        async with DBManager() as db:
            result = await PickupOrdersSyncService().sync_orders_full(db.session)
        logger.info(f"[sync.pickup.orders_full] Synced: {result.get('synced', 0)} orders")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (08) Promotion — Кампании, статистика, акции
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.promotion.campaigns_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_promotion_campaigns_full(self):
    """POST /promotion/sync/campaigns/full — синхронизация рекламных кампаний."""
    from src.services.promotion.sync.campaigns import CampaignsSyncService

    async def _run():
        async with DBManager() as db:
            result = await CampaignsSyncService().sync_campaigns_full(db.session)
        logger.info(f"[sync.promotion.campaigns_full] Synced: {result.get('synced', 0)} campaigns")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.promotion.stats_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_promotion_stats_full(self):
    """POST /promotion/sync/stats/full — синхронизация статистики кампаний."""
    from src.services.promotion.sync.stats import StatsSyncService

    async def _run():
        async with DBManager() as db:
            result = await StatsSyncService().sync_stats_full(db.session)
        logger.info(f"[sync.promotion.stats_full] Synced: {result.get('synced', 0)} stat records")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.promotion.calendar_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_promotion_calendar_full(self):
    """POST /promotion/sync/calendar/full — синхронизация промоакций WB."""
    from src.services.promotion.sync.calendar import CalendarSyncService

    async def _run():
        async with DBManager() as db:
            result = await CalendarSyncService().sync_promotions_full(db.session)
        logger.info(f"[sync.promotion.calendar_full] Synced: {result.get('synced', 0)} promotions")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (09) Communications — Отзывы, вопросы, жалобы
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.communications.feedbacks_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_communications_feedbacks_full(self):
    """POST /communications/sync/feedbacks/full — синхронизация отзывов."""
    from src.services.communications.sync.feedbacks import FeedbacksSyncService

    async def _run():
        async with DBManager() as db:
            result = await FeedbacksSyncService().sync_feedbacks_full(db.session)
        logger.info(f"[sync.communications.feedbacks_full] Synced: {result.get('synced', 0)} feedbacks")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.communications.questions_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_communications_questions_full(self):
    """POST /communications/sync/questions/full — синхронизация вопросов."""
    from src.services.communications.sync.questions import QuestionsSyncService

    async def _run():
        async with DBManager() as db:
            result = await QuestionsSyncService().sync_questions_full(db.session)
        logger.info(f"[sync.communications.questions_full] Synced: {result.get('synced', 0)} questions")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.communications.claims_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_communications_claims_full(self):
    """POST /communications/sync/claims/full — синхронизация жалоб."""
    from src.services.communications.sync.claims import ClaimsSyncService

    async def _run():
        async with DBManager() as db:
            result = await ClaimsSyncService().sync_claims_full(db.session)
        logger.info(f"[sync.communications.claims_full] Synced: {result.get('synced', 0)} claims")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (10) Tariffs — Тарифы (4 отдельных эндпоинта = 4 задачи)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.tariffs.commissions",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_tariffs_commissions(self):
    """POST /tariffs/sync/commissions/ — синхронизация комиссий."""
    from src.services.tariffs.sync.tariffs import TariffsSyncService

    async def _run():
        async with DBManager() as db:
            result = await TariffsSyncService().sync_commissions(db.session)
        logger.info(f"[sync.tariffs.commissions] Synced: {result.get('synced', 0)} commissions")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.tariffs.box",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_tariffs_box(self):
    """POST /tariffs/sync/box/ — синхронизация тарифов коробов."""
    from src.services.tariffs.sync.tariffs import TariffsSyncService

    async def _run():
        async with DBManager() as db:
            result = await TariffsSyncService().sync_box_tariffs(db.session)
        logger.info(f"[sync.tariffs.box] Synced: {result.get('synced', 0)} box tariffs")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.tariffs.pallet",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_tariffs_pallet(self):
    """POST /tariffs/sync/pallet/ — синхронизация тарифов паллет."""
    from src.services.tariffs.sync.tariffs import TariffsSyncService

    async def _run():
        async with DBManager() as db:
            result = await TariffsSyncService().sync_pallet_tariffs(db.session)
        logger.info(f"[sync.tariffs.pallet] Synced: {result.get('synced', 0)} pallet tariffs")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.tariffs.supply",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_tariffs_supply(self):
    """POST /tariffs/sync/supply/ — синхронизация тарифов поставок."""
    from src.services.tariffs.sync.tariffs import TariffsSyncService

    async def _run():
        async with DBManager() as db:
            result = await TariffsSyncService().sync_supply_tariffs(db.session)
        logger.info(f"[sync.tariffs.supply] Synced: {result.get('synced', 0)} supply tariffs")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (12) Reports — Остатки, заказы, продажи (3 отдельных эндпоинта = 3 задачи)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.reports.stocks",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_reports_stocks(self):
    """POST /reports/sync/stocks/ — синхронизация остатков на складах."""
    from src.services.reports.sync.reports import ReportsSyncService

    async def _run():
        async with DBManager() as db:
            result = await ReportsSyncService().sync_stocks(db.session)
        logger.info(f"[sync.reports.stocks] Synced: {result.get('synced', 0)} stock records")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.reports.orders",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_reports_orders(self):
    """POST /reports/sync/orders/ — синхронизация отчёта по заказам."""
    from src.services.reports.sync.reports import ReportsSyncService

    async def _run():
        async with DBManager() as db:
            result = await ReportsSyncService().sync_orders(db.session)
        logger.info(f"[sync.reports.orders] Synced: {result.get('synced', 0)} order reports")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.reports.sales",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_reports_sales(self):
    """POST /reports/sync/sales/ — синхронизация отчёта по продажам."""
    from src.services.reports.sync.reports import ReportsSyncService

    async def _run():
        async with DBManager() as db:
            result = await ReportsSyncService().sync_sales(db.session)
        logger.info(f"[sync.reports.sales] Synced: {result.get('synced', 0)} sale reports")
        return result

    return run_async(_run())


# ---------------------------------------------------------------------------
# (13) Finances — Финансовый отчёт
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.finances.full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_finances_full(self):
    """POST /finances/sync/full/ — синхронизация финансового отчёта."""
    from src.services.finances.sync.finances import FinancesSyncService

    async def _run():
        from datetime import datetime, timedelta
        date_from = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        date_to = datetime.utcnow().strftime("%Y-%m-%d")
        async with DBManager() as db:
            result = await FinancesSyncService().sync_financial_report(db.session, date_from, date_to)
        logger.info(f"[sync.finances.full] Synced: {result.get('synced', 0)} finance records")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.general.users_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_general_users_full(self):
    """POST /general/sync/users/full — полная синхронизация пользователей."""
    from src.services.general.sync.users import UsersSyncService

    async def _run():
        async with DBManager() as db:
            result = await UsersSyncService().sync_users_full(db.session)
        logger.info(f"[sync.general.users_full] Synced: {result.get('synced', 0)} users")
        return result

    return run_async(_run())



# ---------------------------------------------------------------------------
# ИСТОРИЧЕСКИЕ ЗАДАЧИ — запускаются разово для первоначальной загрузки
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.finances.historical",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=120,
    retry_kwargs={"max_retries": 5},
    time_limit=14400,  # 4 часа максимум
)
def sync_finances_historical(self):
    """Полный исторический дамп финансового отчёта за 2 года (по неделям)."""
    from src.services.finances.sync.finances import FinancesSyncService

    async def _run():
        async with DBManager() as db:
            result = await FinancesSyncService().sync_financial_report_historical(db.session)
        logger.info(f"[sync.finances.historical] Done: {result.get('synced', 0)} records, {result.get('weeks')} weeks")
        return result

    return run_async(_run())


@celery_app.task(
    name="sync.feedbacks.historical",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=120,
    retry_kwargs={"max_retries": 5},
    time_limit=21600,  # 6 часов максимум
)
def sync_feedbacks_historical(self):
    """Полный исторический дамп всех отзывов (116k+). Запускается разово."""
    from src.services.communications.sync.feedbacks import FeedbacksSyncService

    async def _run():
        async with DBManager() as db:
            result = await FeedbacksSyncService().sync_feedbacks_historical(db.session)
        logger.info(f"[sync.feedbacks.historical] Done: {result.get('synced', 0)} feedbacks")
        return result

    return run_async(_run())
# ---------------------------------------------------------------------------
# (00) Sync Docs — ежедневная проверка изменений WB API документации
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.docs.wb_api",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_wb_api_docs(self):
    """Скачивает YAML-спеки WB API, сравнивает с сохранёнными версиями, шлёт уведомление при изменениях."""
    import subprocess
    import os
    result = subprocess.run(
        ["python", "-m", "tools", "sync"],
        cwd="/app",
        capture_output=True,
        text=True,
        timeout=240,
    )
    if result.returncode != 0:
        logger.error(f"[sync.docs] Failed:\n{result.stderr[:500]}")
        raise RuntimeError(f"sync_docs exited with code {result.returncode}")
    logger.info(f"[sync.docs] OK:\n{result.stdout[:500]}")
    return {"status": "ok", "output": result.stdout[:500]}



# ---------------------------------------------------------------------------
# FBW Supply Goods - товары в поставках (исторический dump)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.fbw.supply_goods",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
    time_limit=7200,  # 2 часа
)
def sync_fbw_supply_goods(self):
    """Загружает товары для всех поставок FBW из БД (1 запрос на поставку)."""
    from src.collectors.fbw.supplies import FBWSuppliesCollector
    from src.exceptions import WBApiException
    from src.repositories.fbw.supplies import FbwSuppliesRepository, FbwSupplyGoodsRepository

    async def _run():
        async with DBManager() as db:
            supply_repo = FbwSuppliesRepository(db.session)
            goods_repo = FbwSupplyGoodsRepository(db.session)

            # Берём все supply_id из БД
            from sqlalchemy import select, text
            from src.models.fbw import FbwSupply
            result = await db.session.execute(select(FbwSupply.supply_id))
            supply_ids = [row[0] for row in result.all()]

            logger.info(f"[sync.fbw.supply_goods] Loading goods for {len(supply_ids)} supplies")
            total_saved = 0

            async with FBWSuppliesCollector() as collector:
                for idx, supply_id in enumerate(supply_ids):
                    all_goods = []
                    offset = 0
                    while True:
                        try:
                            resp = await collector.get_supply_goods(supply_id=supply_id, limit=1000, offset=offset)
                        except WBApiException as e:
                            if e.status_code == 404:
                                break
                            logger.warning(f"Supply {supply_id}: error {e.status_code}")
                            break
                        goods = resp.goods or []
                        if not goods:
                            break
                        for g in goods:
                            all_goods.append({
                                "supply_id": supply_id,
                                "barcode": g.barcode,
                                "vendor_code": g.article,
                                "name": g.name,
                                "quantity": g.quantity,
                                "brand": g.brand,
                                "subject": g.subject,
                                "raw_data": g.model_dump(),
                            })
                        if len(goods) < 1000:
                            break
                        offset += 1000

                    if all_goods:
                        saved = await goods_repo.upsert_many(all_goods)
                        total_saved += saved

                    if idx % 100 == 0:
                        logger.info(f"[sync.fbw.supply_goods] Progress: {idx}/{len(supply_ids)}, total_saved={total_saved}")

            logger.info(f"[sync.fbw.supply_goods] Done: {total_saved} goods from {len(supply_ids)} supplies")
            return {"synced": total_saved, "supplies": len(supply_ids)}

    return run_async(_run())


# ---------------------------------------------------------------------------
# Promotion Stats - статистика кампаний (rate limit 1 req/min)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.promotion.stats",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=120,
    retry_kwargs={"max_retries": 3},
    time_limit=3600,  # 1 час
    rate_limit="1/m",  # WB лимит: 1 запрос/минута
)
def sync_promotion_stats(self):
    """Статистика рекламных кампаний. Rate limit 1 req/min — 23+ минут на 1113 кампаний."""
    from datetime import datetime, timedelta
    from src.services.promotion.sync.stats import StatsSyncService

    async def _run():
        begin_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
        async with DBManager() as db:
            result = await StatsSyncService().sync_stats(db.session, begin_date=begin_date, end_date=end_date)
        logger.info(f"[sync.promotion.stats] Synced: {result.get('synced', 0)} stats records")
        return result

    return run_async(_run())



# ---------------------------------------------------------------------------
# (03) FBS — Incremental + Passes + Supplies (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.fbs.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_orders_incremental(self):
    from src.services.fbs.sync.orders import FbsOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await FbsOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.fbs.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())


@celery_app.task(
    name="sync.fbs.passes_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_passes_full(self):
    from src.services.fbs.sync.passes import FbsPassesSyncService
    async def _run():
        async with DBManager() as db:
            result = await FbsPassesSyncService().sync_passes(db.session)
        logger.info("[sync.fbs.passes_full] Synced: %d passes", result.get("synced", 0))
        return result
    return run_async(_run())


@celery_app.task(
    name="sync.fbs.supplies_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_supplies_full(self):
    from src.services.fbs.sync.supplies import FbsSuppliesSyncService
    async def _run():
        async with DBManager() as db:
            result = await FbsSuppliesSyncService().sync_supplies(db.session)
        logger.info("[sync.fbs.supplies_full] Synced: %d supplies", result.get("synced", 0))
        return result
    return run_async(_run())


# ---------------------------------------------------------------------------
# (04) DBW — Incremental (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.dbw.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_dbw_orders_incremental(self):
    from src.services.dbw.sync.orders import DbwOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await DbwOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.dbw.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())


# ---------------------------------------------------------------------------
# (05) DBS — Incremental (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.dbs.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_dbs_orders_incremental(self):
    from src.services.dbs.sync.orders import DBSOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await DBSOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.dbs.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())


# ---------------------------------------------------------------------------
# (06) Pickup — Incremental (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.pickup.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_pickup_orders_incremental(self):
    from src.services.pickup.sync.orders import PickupOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await PickupOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.pickup.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())
