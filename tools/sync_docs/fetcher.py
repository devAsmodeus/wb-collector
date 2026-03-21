"""Скачивает YAML файлы с WB API."""
import requests
from pathlib import Path

BASE_URL = "https://dev.wildberries.ru/api/swagger/yaml/ru/"
TIMEOUT  = 15

DOCS = [
    ("01-general",         "Общее"),
    ("02-products",        "Товары"),
    ("03-orders-fbs",      "Заказы FBS"),
    ("04-orders-dbw",      "Заказы DBW"),
    ("05-orders-dbs",      "Заказы DBS"),
    ("06-in-store-pickup", "Самовывоз"),
    ("07-orders-fbw",      "Заказы FBW"),
    ("08-promotion",       "Продвижение"),
    ("09-communications",  "Коммуникации"),
    ("10-tariffs",         "Тарифы"),
    ("11-analytics",       "Аналитика"),
    ("12-reports",         "Отчёты"),
    ("13-finances",        "Финансы"),
]

DOCS_DIR = Path(__file__).parent.parent.parent / "docs" / "api"


def fetch(name: str) -> str | None:
    """Скачивает один YAML файл. Возвращает текст или None при ошибке."""
    try:
        r = requests.get(f"{BASE_URL}{name}.yaml", timeout=TIMEOUT)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def fetch_all() -> dict[str, str | None]:
    """Скачивает все YAML файлы. Возвращает {filename: content}."""
    result = {}
    for name, _ in DOCS:
        result[f"{name}.yaml"] = fetch(name)
    return result


def save(name: str, text: str) -> None:
    """Сохраняет YAML на диск."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / f"{name}.yaml").write_text(text, encoding="utf-8")


def read_local(name: str) -> str | None:
    """Читает локальную копию YAML."""
    path = DOCS_DIR / f"{name}.yaml"
    return path.read_text(encoding="utf-8") if path.exists() else None
