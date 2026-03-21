"""
WB API Docs Tracker
====================
Скачивает YAML-документацию WB, сравнивает с предыдущей версией.

Сравниваются:
  1. SHA256 хэш файла
  2. Семантический снимок: эндпоинты + поля схем

Благодаря семантическому снимку изменение обнаруживается даже если
YAML был обновлён до первого скачивания (новые поля в существующих схемах).

Запуск: python scripts/sync_docs.py
"""

import hashlib
import json
import sys
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    os.system("pip install pyyaml -q")
    import yaml

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

# ─── Конфиг ──────────────────────────────────────────────────────────────────

BASE_URL = "https://dev.wildberries.ru/api/swagger/yaml/ru/"
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

DOCS_DIR = Path(__file__).parent.parent / "docs" / "api"
REPO_DIR = Path(__file__).parent.parent
MANIFEST = DOCS_DIR / "manifest.json"
TIMEOUT  = 15

# Маппинг: имя YAML → папки со схемами/моделями/контроллерами
CHAPTER_MAP = {
    "01-general":         ["src/schemas/general", "src/models/references.py", "src/api/wb/general"],
    "02-products":        ["src/schemas/products", "src/models/products.py",   "src/api/wb/products"],
    "03-orders-fbs":      ["src/schemas/fbs",      "src/models/orders.py",     "src/api/wb/fbs"],
    "04-orders-dbw":      ["src/schemas/dbw",      "src/models/orders.py",     "src/api/wb/dbw"],
    "05-orders-dbs":      ["src/schemas/dbs",      "src/models/orders.py",     "src/api/wb/dbs"],
    "06-in-store-pickup": ["src/schemas/pickup",   "src/models/orders.py",     "src/api/wb/pickup"],
    "07-orders-fbw":      ["src/schemas/fbw",      "src/models/orders.py",     "src/api/wb/fbw"],
    "08-promotion":       ["src/schemas/promotion","src/models/promotion.py",  "src/api/wb/promotion"],
    "09-communications":  ["src/schemas/communications","src/models/communications.py","src/api/wb/communications"],
    "10-tariffs":         ["src/schemas/tariffs",  "src/models/references.py", "src/api/wb/tariffs"],
    "11-analytics":       ["src/schemas/analytics","src/api/wb/analytics"],
    "12-reports":         ["src/schemas/reports",  "src/models/reports.py",    "src/api/wb/reports"],
    "13-finances":        ["src/schemas/finances", "src/models/references.py", "src/api/wb/finances"],
}


# ─── Утилиты ─────────────────────────────────────────────────────────────────

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    return {"files": {}}


def save_manifest(data: dict):
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_yaml(name: str) -> str | None:
    url = f"{BASE_URL}{name}.yaml"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


# ─── Семантический снимок ─────────────────────────────────────────────────────

def extract_schema_fields(schema: dict, depth: int = 0) -> list[str]:
    """Рекурсивно извлекает имена полей схемы (до 2 уровней)."""
    if depth > 2 or not isinstance(schema, dict):
        return []
    fields = []
    props = schema.get("properties", {})
    if isinstance(props, dict):
        fields.extend(props.keys())
        if depth < 1:
            for v in props.values():
                if isinstance(v, dict):
                    fields.extend(extract_schema_fields(v, depth + 1))
    # Поля внутри items (массивы)
    items = schema.get("items", {})
    if isinstance(items, dict) and depth < 1:
        fields.extend(extract_schema_fields(items, depth + 1))
    return fields


def extract_semantics(text: str) -> dict:
    """
    Извлекает семантический снимок из YAML:
    - список эндпоинтов с методами
    - схемы с именами полей
    """
    try:
        d = yaml.safe_load(text)
    except Exception:
        return {}

    # Эндпоинты
    endpoints = {}
    for path, methods in (d.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        http = [m for m in methods if m in ("get", "post", "put", "patch", "delete")]
        if http:
            endpoints[path] = sorted(http)

    # Схемы с полями
    schemas = {}
    comps = (d.get("components") or {}).get("schemas", {})
    for name, schema in (comps or {}).items():
        if isinstance(schema, dict):
            fields = sorted(set(extract_schema_fields(schema)))
            schemas[name] = fields

    return {
        "version":   (d.get("info") or {}).get("version", ""),
        "endpoints": endpoints,
        "schemas":   schemas,
    }


# ─── Diff ────────────────────────────────────────────────────────────────────

def diff_semantics(old: dict, new: dict) -> dict:
    """Сравнивает два семантических снимка, возвращает diff."""
    old_eps = set(old.get("endpoints", {}).keys())
    new_eps = set(new.get("endpoints", {}).keys())

    old_schemas = old.get("schemas", {})
    new_schemas = new.get("schemas", {})

    # Изменения методов на существующих путях
    changed_methods = []
    for path in old_eps & new_eps:
        om = set(old["endpoints"][path])
        nm = set(new["endpoints"][path])
        if om != nm:
            changed_methods.append({
                "path": path,
                "added":   sorted(nm - om),
                "removed": sorted(om - nm),
            })

    # Изменения полей в существующих схемах
    changed_schemas = []
    for name in set(old_schemas.keys()) & set(new_schemas.keys()):
        of = set(old_schemas[name])
        nf = set(new_schemas[name])
        added   = sorted(nf - of)
        removed = sorted(of - nf)
        if added or removed:
            changed_schemas.append({
                "schema":         name,
                "fields_added":   added,
                "fields_removed": removed,
            })

    return {
        "version_changed":   old.get("version") != new.get("version"),
        "old_version":       old.get("version"),
        "new_version":       new.get("version"),
        "endpoints_added":   sorted(new_eps - old_eps),
        "endpoints_removed": sorted(old_eps - new_eps),
        "methods_changed":   changed_methods,
        "schemas_added":     sorted(set(new_schemas) - set(old_schemas)),
        "schemas_removed":   sorted(set(old_schemas) - set(new_schemas)),
        "schemas_changed":   changed_schemas,
    }


def has_changes(diff: dict) -> bool:
    return bool(
        diff["version_changed"] or
        diff["endpoints_added"] or
        diff["endpoints_removed"] or
        diff["methods_changed"] or
        diff["schemas_added"] or
        diff["schemas_removed"] or
        diff["schemas_changed"]
    )


def format_diff(name: str, label: str, diff: dict) -> str:
    lines = [f"📄 {label} ({name})"]

    if diff["version_changed"]:
        lines.append(f"  • Версия: {diff['old_version']} → {diff['new_version']}")

    # Подсказка какие файлы нужно проверить
    affected = CHAPTER_MAP.get(name, [])
    if affected and has_changes(diff):
        lines.append(f"  🗂  Проверьте: {', '.join(affected)}")

    if diff["endpoints_added"]:
        lines.append(f"  ✅ Новые эндпоинты ({len(diff['endpoints_added'])}):")
        for ep in diff["endpoints_added"][:5]:
            lines.append(f"      + {ep}")
        if len(diff["endpoints_added"]) > 5:
            lines.append(f"      ...ещё {len(diff['endpoints_added']) - 5}")

    if diff["endpoints_removed"]:
        lines.append(f"  ❌ Удалённые эндпоинты ({len(diff['endpoints_removed'])}):")
        for ep in diff["endpoints_removed"][:5]:
            lines.append(f"      - {ep}")
        if len(diff["endpoints_removed"]) > 5:
            lines.append(f"      ...ещё {len(diff['endpoints_removed']) - 5}")

    if diff["methods_changed"]:
        lines.append(f"  🔄 Изменены HTTP-методы ({len(diff['methods_changed'])}):")
        for m in diff["methods_changed"][:3]:
            lines.append(f"      {m['path']}")
            if m["added"]:
                lines.append(f"        + {', '.join(m['added'])}")
            if m["removed"]:
                lines.append(f"        - {', '.join(m['removed'])}")

    if diff["schemas_added"]:
        names = ", ".join(diff["schemas_added"][:5])
        extra = f" (+{len(diff['schemas_added'])-5})" if len(diff["schemas_added"]) > 5 else ""
        lines.append(f"  📦 Новые схемы: {names}{extra}")

    if diff["schemas_removed"]:
        names = ", ".join(diff["schemas_removed"][:5])
        lines.append(f"  🗑  Удалённые схемы: {names}")

    if diff["schemas_changed"]:
        lines.append(f"  🔧 Изменены схемы ({len(diff['schemas_changed'])}):")
        for s in diff["schemas_changed"][:5]:
            lines.append(f"      {s['schema']}")
            if s["fields_added"]:
                lines.append(f"        + поля: {', '.join(s['fields_added'])}")
            if s["fields_removed"]:
                lines.append(f"        - поля: {', '.join(s['fields_removed'])}")
        if len(diff["schemas_changed"]) > 5:
            lines.append(f"      ...ещё {len(diff['schemas_changed']) - 5}")

    return "\n".join(lines)


# ─── Главная логика ───────────────────────────────────────────────────────────

def run() -> str:
    manifest = load_manifest()

    # Приводим manifest.files к dict {filename: entry}
    raw_files = manifest.get("files", {})
    if isinstance(raw_files, list):
        old_entries = {f["file"]: f for f in raw_files}
    else:
        old_entries = raw_files

    changed_reports = []
    new_manifest_files = []
    errors = []

    for name, label in DOCS:
        filename = f"{name}.yaml"
        filepath = DOCS_DIR / filename

        new_text = fetch_yaml(name)
        if new_text is None:
            errors.append(filename)
            if filepath.exists():
                old = old_entries.get(filename, {})
                new_manifest_files.append({
                    "file":      filename,
                    "sha256":    old.get("sha256", ""),
                    "size":      filepath.stat().st_size,
                    "semantics": old.get("semantics", {}),
                })
            continue

        new_hash      = sha256(new_text)
        new_semantics = extract_semantics(new_text)
        old_entry     = old_entries.get(filename, {})
        old_hash      = old_entry.get("sha256") if isinstance(old_entry, dict) else old_entry
        old_semantics = old_entry.get("semantics", {}) if isinstance(old_entry, dict) else {}

        new_manifest_files.append({
            "file":      filename,
            "sha256":    new_hash,
            "size":      len(new_text.encode("utf-8")),
            "semantics": new_semantics,
        })

        # ── Сравниваем по хэшу И по семантике ──────────────────────────────
        hash_changed      = old_hash and old_hash != new_hash
        semantics_changed = old_semantics and new_semantics

        if hash_changed or (old_semantics and new_semantics):
            diff = diff_semantics(old_semantics, new_semantics)
            if has_changes(diff):
                changed_reports.append(format_diff(name, label, diff))

        # Сохраняем новую версию файла
        filepath.write_text(new_text, encoding="utf-8")

    # Обновляем манифест
    save_manifest({
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files":      new_manifest_files,
    })

    # Итоговое сообщение
    now     = datetime.now().strftime("%d.%m.%Y %H:%M")
    err_str = f"\n⚠️ Не удалось проверить: {', '.join(errors)}" if errors else ""

    if not changed_reports:
        return f"✅ WB API docs [{now}] — изменений нет. Все {len(DOCS)} глав актуальны.{err_str}"

    report_text   = "\n\n".join(changed_reports)
    changed_names = []
    for r in changed_reports:
        line = r.splitlines()[0]
        if "(" in line and ")" in line:
            changed_names.append(line.split("(")[1].rstrip(")"))

    git_result = git_commit_and_push(changed_names, report_text[:500])

    return (
        f"🔔 WB API docs [{now}] — обнаружены изменения!\n\n"
        f"{report_text}\n\n"
        f"📦 Git: {git_result}\n"
        f"⚙️  Не забудьте: обновить схемы → обновить ORM модели → "
        f"сгенерировать миграцию → закоммитить файл миграции{err_str}"
    )


# ─── Git ─────────────────────────────────────────────────────────────────────

def git(*args) -> tuple[int, str]:
    result = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def git_commit_and_push(changed_files: list[str], summary: str) -> str:
    log = []

    code, out = git("add", "docs/api/")
    log.append("git add: ok" if code == 0 else f"git add err: {out}")

    date_str   = datetime.now().strftime("%Y-%m-%d")
    files_str  = ", ".join(changed_files)
    commit_msg = f"docs: update WB API specs [{date_str}]\n\nChanged: {files_str}\n\n{summary}"

    code, out = git("commit", "-m", commit_msg)
    if code != 0 and "nothing to commit" in out:
        return "git: нечего коммитить"
    log.append(f"git commit: {out.splitlines()[0] if out else 'ok'}")

    code, out = git("push", "origin", "main")
    log.append("git push: ok" if code == 0 else f"git push FAILED: {out[:200]}")

    return " | ".join(log)


# ─── Точка входа ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(run())
