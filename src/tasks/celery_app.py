from celery import Celery
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
        # Расписание заполняется по мере добавления коллекторов
        # "collect-goods-prices": {
        #     "task": "src.tasks.tasks.collect_goods_prices",
        #     "schedule": crontab(minute=0),  # каждый час
        # },
    },
)
