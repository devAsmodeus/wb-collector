"""Исключения приложения + Litestar exception handlers."""
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


def wb_api_handler(_: Request, exc: WBApiException) -> Response:
    if isinstance(exc, WBApiRateLimitException):
        status = HTTP_429_TOO_MANY_REQUESTS
    elif isinstance(exc, WBApiUnauthorizedException):
        status = HTTP_401_UNAUTHORIZED
    else:
        status = HTTP_502_BAD_GATEWAY
    return Response(
        content={"error": "wb_api_error", "status_code": exc.status_code, "detail": exc.message},
        status_code=status,
    )


EXCEPTION_HANDLERS = {
    ObjectNotFoundException: not_found_handler,
    ObjectAlreadyExistsException: already_exists_handler,
    WBApiException: wb_api_handler,
}
