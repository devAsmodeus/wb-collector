"""Скачивание YAML файлов WB API."""
import requests

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


def fetch_yaml(name: str) -> str | None:
    """Скачивает YAML файл по имени главы. Возвращает текст или None при ошибке."""
    url = f"{BASE_URL}{name}.yaml"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def fetch_all() -> dict[str, str | None]:
    """Скачивает все YAML файлы. Возвращает {name: text|None}."""
    return {name: fetch_yaml(name) for name, _ in DOCS}
