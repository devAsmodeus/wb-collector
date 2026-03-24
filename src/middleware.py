"""Middleware для логирования HTTP-запросов."""
import logging
import time
from litestar.middleware import AbstractMiddleware
from litestar.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger("request")


class RequestLoggingMiddleware(AbstractMiddleware):
    """
    Логирует каждый HTTP-запрос:
    - method, path, status, duration_ms, client_ip
    - INFO для 2xx/3xx, WARNING для 4xx, ERROR для 5xx
    """

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.monotonic()
        status_code = 500  # default если send не вызвался

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration_ms = round((time.monotonic() - start) * 1000, 1)
            method = scope.get("method", "?")
            path = scope.get("path", "?")

            # Client IP
            client = scope.get("client")
            client_ip = client[0] if client else "-"

            extra = {
                "method": method,
                "path": path,
                "status": status_code,
                "duration_ms": duration_ms,
                "client_ip": client_ip,
            }

            # Пропускаем health check и метрики чтобы не спамить логи
            if path in ("/health", "/metrics"):
                return

            if status_code >= 500:
                logger.error(f"{method} {path} → {status_code} ({duration_ms}ms)", extra=extra)
            elif status_code >= 400:
                logger.warning(f"{method} {path} → {status_code} ({duration_ms}ms)", extra=extra)
            else:
                logger.info(f"{method} {path} → {status_code} ({duration_ms}ms)", extra=extra)
