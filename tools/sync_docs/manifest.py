"""Работа с manifest.json — хэши + семантические снимки."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

DOCS_DIR = Path(__file__).parent.parent.parent / "docs" / "api"
MANIFEST = DOCS_DIR / "manifest.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_schema_fields(schema: dict, depth: int = 0) -> list[str]:
    """Рекурсивно извлекает имена полей схемы (до 2 уровней)."""
    if depth > 2 or not isinstance(schema, dict):
        return []
    fields = list((schema.get("properties") or {}).keys())
    if depth < 1:
        for v in (schema.get("properties") or {}).values():
            if isinstance(v, dict):
                fields.extend(extract_schema_fields(v, depth + 1))
        items = schema.get("items", {})
        if isinstance(items, dict):
            fields.extend(extract_schema_fields(items, depth + 1))
    return fields


def extract_semantics(text: str) -> dict:
    """Извлекает семантический снимок: эндпоинты + поля схем."""
    try:
        d = yaml.safe_load(text)
    except Exception:
        return {}

    endpoints = {}
    for path, methods in (d.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        http = [m for m in methods if m in ("get", "post", "put", "patch", "delete")]
        if http:
            endpoints[path] = sorted(http)

    schemas = {}
    for name, schema in ((d.get("components") or {}).get("schemas", {}) or {}).items():
        if isinstance(schema, dict):
            schemas[name] = sorted(set(extract_schema_fields(schema)))

    return {
        "version":   (d.get("info") or {}).get("version", ""),
        "endpoints": endpoints,
        "schemas":   schemas,
    }


def load() -> dict:
    """Загружает манифест. Возвращает {filename: entry}."""
    if not MANIFEST.exists():
        return {}
    data = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    files = data.get("files", {})
    if isinstance(files, list):
        return {f["file"]: f for f in files}
    return files


def save(entries: list[dict]) -> None:
    """Сохраняет манифест."""
    MANIFEST.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "files": entries,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def make_entry(filename: str, text: str) -> dict:
    """Создаёт запись манифеста для файла."""
    return {
        "file":      filename,
        "sha256":    sha256(text),
        "size":      len(text.encode("utf-8")),
        "semantics": extract_semantics(text),
    }
