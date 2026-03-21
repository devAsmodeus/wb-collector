"""Чтение и запись manifest.json с хэшами и семантическими снимками."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_PATH = Path(__file__).parent.parent.parent / "docs" / "api" / "manifest.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load() -> dict:
    """Загружает манифест. Возвращает {filename: entry}."""
    if not MANIFEST_PATH.exists():
        return {}
    raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))
    files = raw.get("files", {})
    if isinstance(files, list):
        return {f["file"]: f for f in files}
    return files


def save(entries: list[dict]) -> None:
    """Сохраняет манифест."""
    MANIFEST_PATH.write_text(
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


def build_entry(filename: str, text: str, semantics: dict) -> dict:
    """Создаёт запись для одного файла."""
    return {
        "file":      filename,
        "sha256":    sha256(text),
        "size":      len(text.encode("utf-8")),
        "semantics": semantics,
    }
