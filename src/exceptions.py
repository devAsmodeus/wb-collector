"""Исключения приложения + Litestar exception handlers."""
from __future__ import annotations

import json

from litestar import Request, Response
from litestar.status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_502_BAD_GATEWAY,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_401_UNAUTHORIZED,
)


# ---------------------------------------------------------------------------
# Доменные исключения
# ---------------------------------------------------------------------------

class WBCollectorException(Exception):
    pass


class ObjectNotFoundException(WBCollectorException):
    pass


class ObjectAlreadyExistsException(WBCollectorException):
    pass


class WBApiException(WBCollectorException):
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(f"WB API error {status_code}: {message}")


class WBApiRateLimitException(WBApiException):
    pass


class WBApiUnauthorizedException(WBApiException):
    pass


# ---------------------------------------------------------------------------
# Litestar exception handlers
# ---------------------------------------------------------------------------

def not_found_handler(_: Request, exc: ObjectNotFoundException) -> Response:
    return Response(
        content={"error": "not_found", "detail": str(exc) or "Object not found"},
        status_code=HTTP_404_NOT_FOUND,
    )


def already_exists_handler(_: Request, exc: ObjectAlreadyExistsException) -> Response:
    return Response(
        content={"error": "already_exists", "detail": str(exc)},
        status_code=HTTP_409_CONFLICT,
    )


def _parse_wb_response(raw: str) -> dict | None:
    """Пытается разобрать тело ответа WB как JSON."""
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass
    return None


def _derive_error_type(wb_json: dict | None) -> str:
    """Извлекает тематическое имя ошибки из origin / code / title ответа WB.

    Примеры результатов:
      wb_brands_api_error, wb_content_api_error, wb_marketplace_error, ...
    Если не удалось определить — возвращает generic wb_api_error.
    """
    if not wb_json:
        return "wb_api_error"

    origin = wb_json.get("origin", "") or ""
    if origin:
        # "brands-api" → "wb_brands_api_error"
        slug = origin.replace("-", "_").replace(" ", "_").strip("_")
        return f"wb_{slug}_error"

    code_or_title = wb_json.get("code", "") or wb_json.get("title", "") or ""
    if code_or_title:
        slug = code_or_title.lower().replace(" ", "_").replace("-", "_").strip("_")
        return f"wb_{slug}"

    return "wb_api_error"


def wb_api_handler(_: Request, exc: WBApiException) -> Response:
    """Обработчик ошибок WB API с парсингом реального ответа."""
    if isinstance(exc, WBApiRateLimitException):
        status = HTTP_429_TOO_MANY_REQUESTS
    elif isinstance(exc, WBApiUnauthorizedException):
        status = HTTP_401_UNAUTHORIZED
    else:
        status = HTTP_502_BAD_GATEWAY

    wb_json = _parse_wb_response(exc.message)
    error_type = _derive_error_type(wb_json)

    body: dict = {
        "error": error_type,
        "status_code": exc.status_code,
    }

    if wb_json:
        # Возвращаем реальный JSON от WB, а не строку
        body["wb_response"] = wb_json
    else:
        body["detail"] = exc.message

    return Response(content=body, status_code=status)


EXCEPTION_HANDLERS = {
    ObjectNotFoundException: not_found_handler,
    ObjectAlreadyExistsException: already_exists_handler,
    WBApiException: wb_api_handler,
}
