"""
Базовый HTTP-клиент для WB API.
- Авторизация через Bearer-токен
- Автоматические ретраи (3 попытки)
- Обработка 429 (rate limit) с паузой
- Таймаут на запрос
"""
import asyncio
import logging
from typing import Any

import httpx

from src.config import settings
from src.exceptions import (
    WBApiException,
    WBApiRateLimitException,
    WBApiUnauthorizedException,
)

logger = logging.getLogger(__name__)

RETRY_COUNT = 3
RETRY_DELAY = 2.0       # базовая пауза между ретраями (сек)
RATE_LIMIT_DELAY = 60.0 # пауза при 429 (сек)
REQUEST_TIMEOUT = 30.0  # таймаут одного запроса (сек)


class WBApiClient:
    """
    Асинхронный клиент WB API.

    Использование:
        async with WBApiClient(base_url=settings.WB_PRICES_URL) as client:
            data = await client.get("/api/v2/list/goods/filter", params={"limit": 100})
    """

    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.token = token or settings.WB_API_TOKEN
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": self.token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=REQUEST_TIMEOUT,
        )
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: Any = None,
    ) -> Any:
        """Выполняет запрос с ретраями."""
        last_exc = None

        for attempt in range(1, RETRY_COUNT + 1):
            try:
                response = await self._client.request(
                    method, path, params=params, json=json
                )

                if response.status_code == 200:
                    return response.json()

                if response.status_code == 401:
                    raise WBApiUnauthorizedException(401, "Неверный или просроченный токен")

                if response.status_code == 429:
                    logger.warning(f"Rate limit (попытка {attempt}), ждём {RATE_LIMIT_DELAY}с...")
                    await asyncio.sleep(RATE_LIMIT_DELAY)
                    last_exc = WBApiRateLimitException(429, "Rate limit exceeded")
                    continue

                # Другие ошибки
                body = response.text[:200]
                logger.error(f"WB API {response.status_code}: {path} — {body}")
                raise WBApiException(response.status_code, body)

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                logger.warning(f"Сетевая ошибка (попытка {attempt}/{RETRY_COUNT}): {e}")
                last_exc = e
                if attempt < RETRY_COUNT:
                    await asyncio.sleep(RETRY_DELAY * attempt)

        raise last_exc or WBApiException(0, "Все попытки исчерпаны")

    async def get(self, path: str, params: dict | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: Any = None, params: dict | None = None) -> Any:
        return await self._request("POST", path, json=json, params=params)

    async def put(self, path: str, json: Any = None) -> Any:
        return await self._request("PUT", path, json=json)
