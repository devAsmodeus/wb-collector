import logging
from src.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

# Задачи добавляются здесь по мере разработки коллекторов
# @celery_app.task
# def collect_goods_prices():
#     ...
