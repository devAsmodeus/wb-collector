"""Sync: Reports — Синхронизация отчётов WB в БД (Celery fire-and-forget)."""
from litestar import Controller, post
from src.tasks.celery_app import celery_app


class SyncStocksController(Controller):
    path = "/stocks"
    tags = ["12. Синхронизация"]

    @post(
        "/",
        summary="Синхронизация остатков на складах (Celery)",
        description=(
            "Запускает Celery-задачу для загрузки остатков товаров на складах WB.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/stocks`"
        ),
        status_code=202,
    )
    async def sync_stocks(self) -> dict:
        task = celery_app.send_task("sync.reports.stocks")
        return {"task_id": task.id, "status": "queued", "source": "full"}

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация остатков (Celery)",
        description=(
            "Запускает Celery-задачу для инкременталь��ого обновления остатков.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/stocks`"
        ),
        status_code=202,
    )
    async def sync_stocks_incremental(self) -> dict:
        task = celery_app.send_task("sync.reports.stocks_incremental")
        return {"task_id": task.id, "status": "queued", "source": "incremental"}


class SyncOrdersController(Controller):
    path = "/orders"
    tags = ["12. Синхронизация"]

    @post(
        "/",
        summary="Синхронизация заказов (Celery)",
        description=(
            "Запускает Celery-задачу для загрузки заказов из Statistics API.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/orders`"
        ),
        status_code=202,
    )
    async def sync_orders(self) -> dict:
        task = celery_app.send_task("sync.reports.orders")
        return {"task_id": task.id, "status": "queued", "source": "full"}

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация заказов (Celery)",
        description=(
            "Запускает Celery-задачу для инкрементального обновления заказов.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/orders`"
        ),
        status_code=202,
    )
    async def sync_orders_incremental(self) -> dict:
        task = celery_app.send_task("sync.reports.orders_incremental")
        return {"task_id": task.id, "status": "queued", "source": "incremental"}


class SyncSalesController(Controller):
    path = "/sales"
    tags = ["12. Синхронизация"]

    @post(
        "/",
        summary="Синхронизация продаж и возвратов (Celery)",
        description=(
            "Запускает Celery-задачу для загрузки продаж и возвратов.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/sales`"
        ),
        status_code=202,
    )
    async def sync_sales(self) -> dict:
        task = celery_app.send_task("sync.reports.sales")
        return {"task_id": task.id, "status": "queued", "source": "full"}

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация продаж (Celery)",
        description=(
            "Запускает Celery-задачу для инкрементального обновления продаж.\n\n"
            "**WB:** `GET statistics-api.wildberries.ru/api/v1/supplier/sales`"
        ),
        status_code=202,
    )
    async def sync_sales_incremental(self) -> dict:
        task = celery_app.send_task("sync.reports.sales_incremental")
        return {"task_id": task.id, "status": "queued", "source": "incremental"}
