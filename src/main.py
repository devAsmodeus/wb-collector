import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator

sys.path.append(str(Path(__file__).parent.parent))

# Настроить JSON-логирование ДО всего остального
from src.logging_config import setup_logging
setup_logging(level="INFO")

logger = logging.getLogger(__name__)

from src.init import redis_manager


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="wb-cache")
    logger.info("WB Collector started", extra={"event": "startup"})
    yield
    await redis_manager.close()
    logger.info("WB Collector stopped", extra={"event": "shutdown"})


app = FastAPI(
    title="WB Collector",
    description="Сбор и хранение данных Wildberries API",
    version="0.1.0",
    docs_url=None,
    lifespan=lifespan,
)

# ─── Prometheus метрики (/metrics) ───────────────────────────────────────────
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics", "/health"],
    inprogress_name="http_requests_inprogress",
    inprogress_labels=True,
).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# ─── Роутеры ─────────────────────────────────────────────────────────────────
from src.api.general import router as router_general
from src.api.products import router as router_products

app.include_router(router_general)   # 01 — Общее
app.include_router(router_products)  # 02 — Работа с товарами


# ─── Системные эндпоинты ─────────────────────────────────────────────────────

@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="WB Collector – Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "version": "0.1.0"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
