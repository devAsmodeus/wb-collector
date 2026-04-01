"""
Rate limits из WB API документации (docs/api/*.yaml).

Каждый эндпоинт WB API имеет свой лимит:
- period_sec: период окна (1с, 10с, 60с, 300с, 600с)
- max_requests: макс запросов за период
- interval_sec: минимальный интервал между запросами
- burst: допустимый всплеск

RateLimiter выдерживает interval_sec между запросами к одному эндпоинту.
"""
import asyncio
import time
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RateLimit:
    period_sec: float
    max_requests: int
    interval_sec: float
    burst: int


# ---------------------------------------------------------------------------
# Лимиты из YAML-документации WB API, сгруппированные по host + path prefix.
# Ключ: "{host_short}:{path_prefix}" — матчится по startswith.
# ---------------------------------------------------------------------------

RATE_LIMITS: dict[str, RateLimit] = {

    # ===== (01) General =====
    # common-api.wildberries.ru
    "common-api:/api/communications/v2/news":   RateLimit(60, 10, 60, 10),
    "common-api:/api/v1/seller-info":           RateLimit(60, 10, 60, 10),
    "common-api:/ping":                         RateLimit(30, 3, 10, 3),
    # user-management-api.wildberries.ru
    "user-management-api:/api/v1/invite":       RateLimit(1, 5, 0.2, 5),
    "user-management-api:/api/v1/users":        RateLimit(1, 5, 0.2, 5),
    "user-management-api:/api/v1/user":         RateLimit(1, 10, 0.1, 10),

    # ===== (02) Products =====
    # content-api.wildberries.ru
    "content-api:/content/v2/get/cards/list":       RateLimit(60, 100, 0.6, 5),
    "content-api:/content/v2/cards":                RateLimit(60, 10, 6, 5),
    "content-api:/content/v2/cards/trash":           RateLimit(60, 3, 20, 5),
    "content-api:/content/v2/cards/error/list":     RateLimit(60, 10, 6, 5),
    "content-api:/content/v2/cards/limits":         RateLimit(60, 100, 0.6, 5),
    "content-api:/content/v2/barcodes":             RateLimit(60, 100, 0.6, 5),
    "content-api:/content/v2/tag":                  RateLimit(60, 100, 0.6, 5),
    "content-api:/content/v2/directory":            RateLimit(60, 100, 0.6, 5),
    "content-api:/content/v2/object":               RateLimit(60, 100, 0.6, 5),
    "content-api:/content/v2/brands":               RateLimit(1, 1, 1, 5),
    # discounts-prices-api.wildberries.ru
    "discounts-prices-api:/api/v2/list/goods":      RateLimit(60, 100, 0.6, 5),
    "discounts-prices-api:/api/v2/upload":           RateLimit(60, 100, 0.6, 5),
    "discounts-prices-api:/api/v2/history":          RateLimit(60, 100, 0.6, 5),
    # marketplace-api.wildberries.ru (stocks, warehouses)
    "marketplace-api:/api/v3/stocks":               RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/warehouses":            RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/offices":               RateLimit(60, 300, 0.2, 20),

    # ===== (03) FBS Orders =====
    "marketplace-api:/api/v3/orders":               RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/supplies":              RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/passes":                RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/orders/cancel":         RateLimit(60, 100, 0.6, 20),
    "marketplace-api:/api/v3/orders/stickers":       RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/orders/metacomm":       RateLimit(60, 300, 0.2, 20),
    # FBS markings (SGTIN, UIN, IMEI, GTIN)
    "marketplace-api:/api/v3/orders/sgtin":          RateLimit(60, 1000, 0.06, 20),
    "marketplace-api:/api/v3/orders/uin":            RateLimit(60, 1000, 0.06, 20),
    "marketplace-api:/api/v3/orders/imei":           RateLimit(60, 1000, 0.06, 20),
    "marketplace-api:/api/v3/orders/gtin":           RateLimit(60, 1000, 0.06, 20),
    "marketplace-api:/api/v3/orders/expiration":     RateLimit(60, 1000, 0.06, 20),
    "marketplace-api:/api/v3/orders/customs":        RateLimit(60, 1000, 0.06, 20),

    # ===== (04) DBW Orders =====
    "marketplace-api:/api/v3/dbw":                  RateLimit(60, 300, 0.2, 20),

    # ===== (05) DBS Orders =====
    "marketplace-api:/api/v3/dbs/orders":           RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/dbs/orders/cancel":    RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/dbs/orders/confirm":   RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/dbs/orders/deliver":   RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/dbs/orders/receive":   RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/dbs/orders/reject":    RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/dbs/orders/meta":      RateLimit(60, 150, 0.4, 20),
    "marketplace-api:/api/v3/dbs/orders/sgtin":     RateLimit(60, 500, 0.12, 20),
    "marketplace-api:/api/v3/dbs/orders/uin":       RateLimit(60, 500, 0.12, 20),
    "marketplace-api:/api/v3/dbs/orders/imei":      RateLimit(60, 500, 0.12, 20),
    "marketplace-api:/api/v3/dbs/orders/gtin":      RateLimit(60, 500, 0.12, 20),
    "marketplace-api:/api/v3/dbs/orders/customs":   RateLimit(60, 500, 0.12, 20),

    # ===== (06) Pickup =====
    "marketplace-api:/api/v3/pickup/orders":          RateLimit(60, 300, 0.2, 20),
    "marketplace-api:/api/v3/pickup/orders/confirm":  RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/pickup/orders/prepare":  RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/pickup/orders/receive":  RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/pickup/orders/reject":   RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/pickup/orders/cancel":   RateLimit(1, 1, 1, 10),
    "marketplace-api:/api/v3/pickup/orders/check":    RateLimit(60, 30, 2, 20),
    "marketplace-api:/api/v3/pickup/orders/meta":     RateLimit(60, 150, 0.4, 20),
    "marketplace-api:/api/v3/pickup/orders/sgtin":    RateLimit(60, 20, 3, 500),
    "marketplace-api:/api/v3/pickup/orders/uin":      RateLimit(60, 20, 3, 500),
    "marketplace-api:/api/v3/pickup/orders/imei":     RateLimit(60, 20, 3, 500),
    "marketplace-api:/api/v3/pickup/orders/gtin":     RateLimit(60, 20, 3, 500),

    # ===== (07) FBW =====
    "marketplace-api:/api/v3/acceptance":             RateLimit(60, 6, 10, 6),
    "marketplace-api:/api/v3/supply":                 RateLimit(60, 30, 2, 10),

    # ===== (08) Promotion =====
    # advert-api.wildberries.ru
    "advert-api:/adv/v1/promotion/count":       RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v1/promotion/adverts":     RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v2/adverts":               RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v1/budget":                RateLimit(1, 4, 0.25, 4),
    "advert-api:/adv/v1/balance":               RateLimit(1, 1, 1, 5),
    "advert-api:/adv/v1/fullstats":             RateLimit(60, 3, 20, 1),
    "advert-api:/adv/v2/fullstats":             RateLimit(60, 3, 20, 1),
    "advert-api:/adv/v1/stat":                  RateLimit(60, 3, 20, 1),
    "advert-api:/adv/v1/auto/daily-words":      RateLimit(60, 10, 6, 20),
    "advert-api:/adv/v1/search/set-plus":       RateLimit(1, 2, 0.5, 4),
    "advert-api:/adv/v0/count":                 RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/advert":                RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/adverts":               RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/start":                 RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/pause":                 RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/stop":                  RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/delete":                RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/rename":                RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v0/params":                RateLimit(1, 1, 1, 1),
    "advert-api:/adv/v0/cpm":                   RateLimit(1, 1, 1, 1),
    "advert-api:/adv/v0/nm":                    RateLimit(1, 1, 1, 1),
    "advert-api:/adv/v1/save":                  RateLimit(60, 5, 12, 5),
    "advert-api:/adv/v1/nms":                   RateLimit(60, 5, 12, 5),
    "advert-api:/adv/v1/min-cpm":               RateLimit(60, 20, 3, 5),
    "advert-api:/adv/v1/subject":               RateLimit(12, 1, 12, 5),
    # Promotion calendar
    "advert-api:/adv/v2/promotion":              RateLimit(1, 5, 0.2, 5),
    "advert-api:/adv/v1/promotion/nomenclatures": RateLimit(1, 5, 0.2, 5),

    # ===== (09) Communications =====
    # feedbacks-api.wildberries.ru
    "feedbacks-api:/api/v1/feedbacks":          RateLimit(1, 3, 0.333, 6),
    "feedbacks-api:/api/v1/questions":          RateLimit(1, 3, 0.333, 6),
    "feedbacks-api:/api/v1/new-feedbacks-questions": RateLimit(1, 3, 0.333, 6),
    "feedbacks-api:/api/v1/pins":               RateLimit(1, 3, 0.333, 6),
    # Chat
    "marketplace-api:/api/v2/chat":             RateLimit(10, 10, 1, 10),
    # Claims
    "marketplace-api:/api/v1/claims":           RateLimit(60, 20, 3, 10),

    # ===== (10) Tariffs =====
    # common-api.wildberries.ru
    "common-api:/api/v1/tariffs/commission":    RateLimit(60, 1, 60, 2),
    "common-api:/api/v1/tariffs/box":           RateLimit(60, 60, 1, 5),
    "common-api:/api/v1/tariffs/pallet":        RateLimit(60, 60, 1, 5),
    "common-api:/api/v1/tariffs/return":        RateLimit(60, 60, 1, 5),
    "common-api:/api/v1/tariffs/supply":        RateLimit(60, 6, 10, 6),

    # ===== (11) Analytics =====
    # seller-analytics-api.wildberries.ru
    "seller-analytics-api:/api/v2/nm-report":   RateLimit(60, 3, 20, 3),
    "seller-analytics-api:/api/v1/analytics":   RateLimit(60, 3, 20, 3),
    "seller-analytics-api:/api/v2/analytics":   RateLimit(60, 3, 20, 3),

    # ===== (12) Reports =====
    # statistics-api.wildberries.ru
    "statistics-api:/api/v1/supplier/stocks":    RateLimit(60, 1, 60, 1),
    "statistics-api:/api/v1/supplier/orders":    RateLimit(60, 1, 60, 1),
    "statistics-api:/api/v1/supplier/sales":     RateLimit(60, 1, 60, 1),
    "statistics-api:/api/v5/supplier/reportDetailByPeriod": RateLimit(60, 1, 60, 1),
    # seller-analytics-api (reports)
    "seller-analytics-api:/api/v1/paid_storage": RateLimit(60, 1, 60, 1),
    "seller-analytics-api:/api/v1/analytics/acceptance-report": RateLimit(60, 1, 60, 5),
    "seller-analytics-api:/api/v1/analytics/antifraud-details": RateLimit(600, 1, 600, 10),
    "seller-analytics-api:/api/v1/analytics/blocked-products": RateLimit(10, 1, 10, 6),
    "seller-analytics-api:/api/v1/analytics/brand-parent-subjects": RateLimit(5, 1, 5, 20),
    "seller-analytics-api:/api/v1/analytics/seller-brands": RateLimit(60, 1, 60, 10),

    # ===== (13) Finances =====
    # common-api.wildberries.ru
    "common-api:/api/v1/balance":               RateLimit(60, 1, 60, 1),
    # finance-api.wildberries.ru (если отдельный хост)
    "finance-api:/api/v1/documents":            RateLimit(10, 1, 10, 5),
    "finance-api:/api/v1/documents/download":   RateLimit(300, 1, 300, 5),
}

# Fallback лимит для неизвестных эндпоинтов
DEFAULT_RATE_LIMIT = RateLimit(60, 100, 0.6, 5)


class RateLimiter:
    """
    Трекер rate limits. Перед каждым запросом вызывает wait_if_needed(),
    который выдерживает interval_sec между запросами к одному эндпоинту.
    """

    def __init__(self):
        self._last_request: dict[str, float] = {}

    def _find_limit(self, host: str, path: str) -> tuple[str, RateLimit]:
        """Ищет подходящий лимит по host:path_prefix (longest prefix match)."""
        host_short = host.replace("https://", "").replace("http://", "").split(".wildberries.ru")[0]

        best_key = None
        best_len = 0

        for key, limit in RATE_LIMITS.items():
            key_host, key_path = key.split(":", 1)
            if host_short == key_host and path.startswith(key_path):
                if len(key_path) > best_len:
                    best_key = key
                    best_len = len(key_path)

        if best_key:
            return best_key, RATE_LIMITS[best_key]
        return f"{host_short}:*", DEFAULT_RATE_LIMIT

    async def wait_if_needed(self, host: str, path: str) -> None:
        """Выдерживает интервал между запросами к одному эндпоинту."""
        key, limit = self._find_limit(host, path)
        now = time.monotonic()
        last = self._last_request.get(key, 0)
        elapsed = now - last

        if elapsed < limit.interval_sec:
            wait_time = limit.interval_sec - elapsed
            logger.debug(
                f"Rate limit: waiting {wait_time:.2f}s before {path}",
                extra={"key": key, "interval": limit.interval_sec},
            )
            await asyncio.sleep(wait_time)

        self._last_request[key] = time.monotonic()


# Глобальный экземпляр — один на всё приложение
rate_limiter = RateLimiter()
