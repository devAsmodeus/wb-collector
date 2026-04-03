from celery import Celery
from celery.schedules import crontab
from src.config import settings

celery_app = Celery(
    "wb_collector",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["src.tasks.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Minsk",
    enable_utc=True,
    beat_schedule={

        # =================================================================
        # (01) General — Продавец + Новости
        # =================================================================

        # Продавец — раз в сутки, данные почти не меняются
        "sync-general-seller-full": {
            "task": "sync.general.seller_full",
            "schedule": crontab(minute=0, hour=5),   # 05:00
        },
        # Новости — инкрементально раз в сутки
        "sync-general-news-full": {
            "task": "sync.general.news_full",
            "schedule": crontab(minute=5, hour=5),   # 05:05 (раз в неделю полная)
        },
        "sync-general-news-incremental": {
            "task": "sync.general.news_incremental",
            "schedule": crontab(minute=10, hour=5),  # 05:10 (ежедневно)
        },
        "sync-general-users-full": {
            "task": "sync.general.users_full",
            "schedule": crontab(minute=15, hour=5),  # 05:15 (ежедневно)
        },

        # =================================================================
        # (02) Products — Карточки, цены, теги, склады, справочники
        # =================================================================

        # Карточки — каждый час, данные часто обновляются
        "sync-products-cards-full": {
            "task": "sync.products.cards_full",
            "schedule": crontab(minute=5),            # :05 каждого часа
        },
        # Цены — каждый час
        "sync-products-prices-full": {
            "task": "sync.products.prices_full",
            "schedule": crontab(minute=10),           # :10 каждого часа
        },
        # Теги — раз в сутки, меняются редко
        "sync-products-tags-full": {
            "task": "sync.products.tags_full",
            "schedule": crontab(minute=20, hour=4),  # 04:20
        },
        # Склады — раз в сутки
        "sync-products-warehouses-full": {
            "task": "sync.products.warehouses_full",
            "schedule": crontab(minute=25, hour=4),  # 04:25
        },
        # Категории — раз в сутки, справочник
        "sync-products-directories-categories": {
            "task": "sync.products.directories_categories",
            "schedule": crontab(minute=15, hour=4),  # 04:15
        },
        # Предметы — раз в сутки, справочник
        "sync-products-directories-subjects": {
            "task": "sync.products.directories_subjects",
            "schedule": crontab(minute=17, hour=4),  # 04:17
        },

        # =================================================================
        # (03) FBS — Заказы
        # =================================================================

        "sync-fbs-orders-full": {
            "task": "sync.fbs.orders_full",
            "schedule": crontab(minute="*/15"),       # каждые 15 мин
        },

        # =================================================================
        # (04) DBW — Заказы
        # =================================================================

        "sync-dbw-orders-full": {
            "task": "sync.dbw.orders_full",
            "schedule": crontab(minute="*/15"),       # каждые 15 мин
        },

        # =================================================================
        # (05) DBS — Заказы
        # =================================================================

        "sync-dbs-orders-full": {
            "task": "sync.dbs.orders_full",
            "schedule": crontab(minute="*/15"),       # каждые 15 мин
        },

        # =================================================================
        # (06) Pickup — Заказы
        # =================================================================

        "sync-pickup-orders-full": {
            "task": "sync.pickup.orders_full",
            "schedule": crontab(minute="*/15"),       # каждые 15 мин
        },

        # =================================================================
        # (08) Promotion — Кампании, статистика, акции
        # =================================================================

        # Кампании — каждые 3 часа
        "sync-promotion-campaigns-full": {
            "task": "sync.promotion.campaigns_full",
            "schedule": crontab(minute=20, hour="*/3"),  # :20 каждые 3 часа
        },
        # Статистика — каждые 3 часа
        "sync-promotion-stats-full": {
            "task": "sync.promotion.stats_full",
            "schedule": crontab(minute=25, hour="*/3"),  # :25 каждые 3 часа
        },
        # Промоакции/календарь — раз в сутки
        "sync-promotion-calendar-full": {
            "task": "sync.promotion.calendar_full",
            "schedule": crontab(minute=30, hour=4),  # 04:30
        },

        # =================================================================
        # (09) Communications — Отзывы, вопросы, жалобы
        # =================================================================

        # Отзывы — каждые 30 мин
        "sync-communications-feedbacks-full": {
            "task": "sync.communications.feedbacks_full",
            "schedule": crontab(minute="7,37"),       # :07 и :37
        },
        # Вопросы — каждые 30 мин
        "sync-communications-questions-full": {
            "task": "sync.communications.questions_full",
            "schedule": crontab(minute="12,42"),      # :12 и :42
        },
        # Жалобы — каждые 30 мин
        "sync-communications-claims-full": {
            "task": "sync.communications.claims_full",
            "schedule": crontab(minute="17,47"),      # :17 и :47
        },

        # =================================================================
        # (10) Tariffs — 4 вида тарифов = 4 задачи
        # =================================================================

        # Комиссии — раз в сутки
        "sync-tariffs-commissions": {
            "task": "sync.tariffs.commissions",
            "schedule": crontab(minute=0, hour=4),   # 04:00
        },
        # Тарифы коробов — раз в сутки
        "sync-tariffs-box": {
            "task": "sync.tariffs.box",
            "schedule": crontab(minute=3, hour=4),   # 04:03
        },
        # Тарифы паллет — раз в сутки
        "sync-tariffs-pallet": {
            "task": "sync.tariffs.pallet",
            "schedule": crontab(minute=6, hour=4),   # 04:06
        },
        # Тарифы поставок — раз в сутки
        "sync-tariffs-supply": {
            "task": "sync.tariffs.supply",
            "schedule": crontab(minute=9, hour=4),   # 04:09
        },

        # =================================================================
        # (12) Reports — 3 вида отчётов = 3 задачи
        # =================================================================

        # Остатки — раз в сутки
        "sync-reports-stocks": {
            "task": "sync.reports.stocks",
            "schedule": crontab(minute=0, hour=3),   # 03:00
        },
        # Отчёт по заказам — раз в сутки
        "sync-reports-orders": {
            "task": "sync.reports.orders",
            "schedule": crontab(minute=15, hour=3),  # 03:15
        },
        # Отчёт по продажам — раз в сутки
        "sync-reports-sales": {
            "task": "sync.reports.sales",
            "schedule": crontab(minute=30, hour=3),  # 03:30
        },

        # =================================================================
        # (13) Finances — Финансовый отчёт
        # =================================================================

        "sync-finances-full": {
            "task": "sync.finances.full",
            "schedule": crontab(minute=45, hour=3),  # 03:45
        },

        # =================================================================
        # (00) Sync Docs — ежедневная проверка изменений WB API
        # =================================================================

        "sync-docs-wb-api": {
            "task": "sync.docs.wb_api",
            "schedule": crontab(minute=0, hour=8),   # 08:00 ежедневно
        },
    },
)
