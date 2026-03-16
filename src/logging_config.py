"""
Конфигурация логирования.

Логи пишутся в stdout в JSON-формате — Docker пишет их в свой journal,
откуда Promtail читает и отправляет в Loki.

Пример лог-записи:
{
  "timestamp": "2026-03-16T15:00:00.000Z",
  "level": "INFO",
  "logger": "src.collectors.products.prices",
  "message": "Собрано 100 товаров",
  "module": "prices",
  "request_id": "abc123"
}
"""
import logging
import sys
from pythonjsonlogger.jsonlogger import JsonFormatter


def setup_logging(level: str = "INFO") -> None:
    """Настроить JSON-логирование в stdout."""

    # Форматтер: каждая строка лога = один JSON-объект
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level",
            "name": "logger",
            "message": "message",
        },
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Корневой логгер
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers.clear()
    root.addHandler(handler)

    # Приглушить шумные либы
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
