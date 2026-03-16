"""
Кастомные Prometheus метрики для wb-collector.

Метрики автоматически доступны на /metrics (добавляются к стандартным
HTTP-метрикам от prometheus-fastapi-instrumentator).

Использование в коллекторах:
    from src.metrics import WB_API_REQUESTS, WB_API_ERRORS, record_collection

    WB_API_REQUESTS.labels(host="discounts-prices-api.wildberries.ru", method="GET").inc()
    record_collection("prices", items_count=100, duration_seconds=1.5)
"""
from prometheus_client import Counter, Histogram, Gauge

# ─── WB API вызовы ───────────────────────────────────────────────────────────

WB_API_REQUESTS = Counter(
    name="wb_api_requests_total",
    documentation="Всего запросов к WB API",
    labelnames=["host", "method", "status"],
)
# Использование: WB_API_REQUESTS.labels(host="...", method="GET", status="200").inc()

WB_API_ERRORS = Counter(
    name="wb_api_errors_total",
    documentation="Ошибки WB API по типу",
    labelnames=["host", "error_type"],
)
# error_type: rate_limit | unauthorized | timeout | server_error

WB_API_RESPONSE_TIME = Histogram(
    name="wb_api_response_seconds",
    documentation="Время ответа WB API",
    labelnames=["host", "endpoint"],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)

WB_RATE_LIMIT_HITS = Counter(
    name="wb_rate_limit_hits_total",
    documentation="Кол-во 429 от WB API",
    labelnames=["host"],
)

# ─── Сбор данных ─────────────────────────────────────────────────────────────

COLLECTION_RUNS = Counter(
    name="wb_collection_runs_total",
    documentation="Запуски коллекторов",
    labelnames=["module", "status"],  # status: success | error
)

COLLECTION_ITEMS = Counter(
    name="wb_collection_items_total",
    documentation="Собрано записей",
    labelnames=["module"],
)

COLLECTION_DURATION = Histogram(
    name="wb_collection_duration_seconds",
    documentation="Время работы коллектора",
    labelnames=["module"],
    buckets=[1, 5, 15, 30, 60, 120, 300, 600],
)

LAST_COLLECTION_TIMESTAMP = Gauge(
    name="wb_last_collection_timestamp",
    documentation="Unix timestamp последнего успешного сбора",
    labelnames=["module"],
)

# ─── Хелпер ──────────────────────────────────────────────────────────────────

def record_collection(module: str, items_count: int, duration_seconds: float, success: bool = True) -> None:
    """Зафиксировать результат запуска коллектора."""
    import time
    status = "success" if success else "error"
    COLLECTION_RUNS.labels(module=module, status=status).inc()
    if items_count > 0:
        COLLECTION_ITEMS.labels(module=module).inc(items_count)
    COLLECTION_DURATION.labels(module=module).observe(duration_seconds)
    if success:
        LAST_COLLECTION_TIMESTAMP.labels(module=module).set(time.time())
