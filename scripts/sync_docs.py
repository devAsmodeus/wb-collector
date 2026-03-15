"""
WB API Docs Tracker
====================
Скачивает YAML-документацию WB, сравнивает с предыдущей версией,
выводит краткий отчёт об изменениях.

Запуск: python scripts/sync_docs.py
Вывод:  JSON в stdout (для OpenClaw cron)
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
    ("01-general",        "Общее"),
    ("02-products",       "Товары"),
    ("03-orders-fbs",     "Заказы FBS"),
    ("04-orders-dbw",     "Заказы DBW"),
    ("05-orders-dbs",     "Заказы DBS"),
    ("06-in-store-pickup","Самовывоз"),
    ("07-orders-fbw",     "Заказы FBW"),
    ("08-promotion",      "Продвижение"),
    ("09-communications", "Коммуникации"),
    ("10-tariffs",        "Тарифы"),
    ("11-analytics",      "Аналитика"),
    ("12-reports",        "Отчёты"),
    ("13-finances",       "Финансы"),
]

DOCS_DIR   = Path(__file__).parent.parent / "docs" / "api"
REPO_DIR   = Path(__file__).parent.parent
MANIFEST   = DOCS_DIR / "manifest.json"
TIMEOUT    = 15


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
    except Exception as e:
        return None


# ─── Семантический diff ───────────────────────────────────────────────────────

def parse_spec(text: str) -> dict:
    """Извлекаем ключевые элементы из OpenAPI YAML."""
    try:
        d = yaml.safe_load(text)
    except Exception:
        return {}

    paths = {}
    for path, methods in (d.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        http_methods = [m for m in methods if m in ("get","post","put","patch","delete")]
        paths[path] = http_methods

    schemas = list((d.get("components") or {}).get("schemas", {}).keys())

    return {
        "title":   (d.get("info") or {}).get("title", ""),
        "version": (d.get("info") or {}).get("version", ""),
        "paths":   paths,
        "schemas": schemas,
    }


def diff_specs(old_text: str, new_text: str) -> dict:
    """Сравниваем два YAML, возвращаем краткий diff."""
    old = parse_spec(old_text)
    new = parse_spec(new_text)

    old_paths = set(old.get("paths", {}).keys())
    new_paths = set(new.get("paths", {}).keys())

    old_schemas = set(old.get("schemas", []))
    new_schemas = set(new.get("schemas", []))

    # Изменения методов на существующих путях
    changed_methods = []
    for path in old_paths & new_paths:
        om = set(old["paths"][path])
        nm = set(new["paths"][path])
        added   = nm - om
        removed = om - nm
        if added or removed:
            changed_methods.append({
                "path": path,
                "added_methods":   sorted(added),
                "removed_methods": sorted(removed),
            })

    return {
        "endpoints_added":   sorted(new_paths - old_paths),
        "endpoints_removed": sorted(old_paths - new_paths),
        "methods_changed":   changed_methods,
        "schemas_added":     sorted(new_schemas - old_schemas),
        "schemas_removed":   sorted(old_schemas - new_schemas),
        "version_changed":   old.get("version") != new.get("version"),
        "old_version":       old.get("version"),
        "new_version":       new.get("version"),
    }


def has_changes(diff: dict) -> bool:
    return bool(
        diff["endpoints_added"] or
        diff["endpoints_removed"] or
        diff["methods_changed"] or
        diff["schemas_added"] or
        diff["schemas_removed"] or
        diff["version_changed"]
    )


def format_diff(name: str, label: str, diff: dict) -> str:
    """Форматируем diff в читаемый текст."""
    lines = [f"📄 {label} ({name})"]

    if diff["version_changed"]:
        lines.append(f"  • Версия: {diff['old_version']} → {diff['new_version']}")

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
        lines.append(f"  🔄 Изменены методы ({len(diff['methods_changed'])}):")
        for m in diff["methods_changed"][:3]:
            lines.append(f"      {m['path']}")
            if m["added_methods"]:
                lines.append(f"        + {', '.join(m['added_methods'])}")
            if m["removed_methods"]:
                lines.append(f"        - {', '.join(m['removed_methods'])}")

    if diff["schemas_added"]:
        lines.append(f"  📦 Новые схемы: {', '.join(diff['schemas_added'][:5])}")
        if len(diff["schemas_added"]) > 5:
            lines.append(f"      ...ещё {len(diff['schemas_added']) - 5}")

    if diff["schemas_removed"]:
        lines.append(f"  🗑  Удалённые схемы: {', '.join(diff['schemas_removed'][:5])}")

    return "\n".join(lines)


# ─── Главная логика ───────────────────────────────────────────────────────────

def run() -> str:
    manifest = load_manifest()
    old_hashes = {f["file"]: f for f in manifest.get("files", [])} \
        if isinstance(manifest.get("files"), list) \
        else manifest.get("files", {})

    changed_reports = []
    new_manifest_files = []
    errors = []

    for name, label in DOCS:
        filename = f"{name}.yaml"
        filepath = DOCS_DIR / filename

        new_text = fetch_yaml(name)
        if new_text is None:
            errors.append(filename)
            # Оставляем старый файл
            if filepath.exists():
                new_manifest_files.append({
                    "file": filename,
                    "sha256": old_hashes.get(filename, {}).get("sha256", ""),
                    "size": filepath.stat().st_size,
                })
            continue

        new_hash = sha256(new_text)
        old_entry = old_hashes.get(filename, {})
        old_hash = old_entry.get("sha256") if isinstance(old_entry, dict) else old_entry

        new_manifest_files.append({
            "file": filename,
            "sha256": new_hash,
            "size": len(new_text.encode("utf-8")),
        })

        if old_hash and old_hash != new_hash:
            # Есть изменения — читаем старый файл для diff
            if filepath.exists():
                old_text = filepath.read_text(encoding="utf-8")
                diff = diff_specs(old_text, new_text)
                if has_changes(diff):
                    changed_reports.append(format_diff(name, label, diff))

        # Сохраняем новую версию
        filepath.write_text(new_text, encoding="utf-8")

    # Обновляем манифест
    save_manifest({
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": new_manifest_files,
    })

    # Формируем итоговое сообщение
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    err_str = f"\n⚠️ Не удалось проверить: {', '.join(errors)}" if errors else ""

    if not changed_reports:
        return f"✅ WB API docs [{now}] — изменений нет. Все {len(DOCS)} глав актуальны.{err_str}"

    # Есть изменения — коммитим и пушим
    report_text = "\n\n".join(changed_reports)
    changed_names = [r.splitlines()[0].split("(")[1].rstrip(")") for r in changed_reports]

    git_result = git_commit_and_push(changed_names, report_text[:500])

    return (
        f"🔔 WB API docs [{now}] — обнаружены изменения!\n\n"
        f"{report_text}\n\n"
        f"📦 Git: {git_result}{err_str}"
    )


# ─── Git ─────────────────────────────────────────────────────────────────────

def git(*args) -> tuple[int, str]:
    """Запускает git команду в директории проекта."""
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
    """Коммитит изменённые файлы и пушит в remote."""
    log = []

    # git add
    code, out = git("add", "docs/api/")
    log.append(f"git add: {out or 'ok'}" if code != 0 else "git add: ok")

    # Формируем сообщение коммита
    date_str = datetime.now().strftime("%Y-%m-%d")
    files_str = ", ".join(changed_files)
    commit_msg = f"docs: update WB API specs [{date_str}]\n\nChanged: {files_str}\n\n{summary}"

    code, out = git("commit", "-m", commit_msg)
    if code != 0 and "nothing to commit" in out:
        return "git: нечего коммитить"
    log.append(f"git commit: {out.splitlines()[0] if out else 'ok'}")

    # git push
    code, out = git("push", "origin", "main")
    if code != 0:
        log.append(f"git push FAILED: {out[:200]}")
    else:
        log.append("git push: ok")

    return " | ".join(log)


# ─── Точка входа ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    result = run()
    print(result)
