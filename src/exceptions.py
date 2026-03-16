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
