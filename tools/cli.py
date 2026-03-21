"""
WB Collector Tools — полный проход по всем инструментам.

Запуск:
  python -m tools            → полный проход (migrate + sync_docs + drift)
  python -m tools migrate    → только миграции
  python -m tools sync       → только синхронизация документации
  python -m tools drift      → только проверка дрейфа схем
"""
import sys
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent

SEPARATOR = "─" * 60


def section(title: str) -> None:
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def run_migrate() -> tuple[bool, str]:
    """Запускает alembic upgrade head."""
    from tools.migrate.runner import run_migrations
    result = run_migrations()
    if result["status"] == "up_to_date":
        return True, "✅ Миграции — БД актуальна, нечего применять."
    elif result["success"]:
        return True, f"✅ Миграции применены: {result['status']}\n{result['output']}"
    else:
        return False, f"❌ Ошибка миграций:\n{result['output']}"


def run_sync() -> tuple[bool, str]:
    """Запускает синхронизацию YAML документации."""
    from tools.sync_docs.fetcher import DOCS, fetch_yaml
    from tools.sync_docs.manifest import load, save, make_entry, sha256
    from tools.sync_docs.differ import diff, has_changes
    from tools.sync_docs.notifier import format_diff

    DOCS_DIR = REPO_DIR / "docs" / "api"

    old_entries = load()
    changed_reports = []
    new_entries = []
    errors = []

    for name, label in DOCS:
        filename = f"{name}.yaml"
        filepath = DOCS_DIR / filename

        new_text = fetch_yaml(name)
        if new_text is None:
            errors.append(filename)
            if filepath.exists():
                old = old_entries.get(filename, {})
                new_entries.append({
                    "file":      filename,
                    "sha256":    old.get("sha256", ""),
                    "size":      filepath.stat().st_size,
                    "semantics": old.get("semantics", {}),
                })
            continue

        entry = make_entry(filename, new_text)
        new_entries.append(entry)

        old_entry     = old_entries.get(filename, {})
        old_hash      = old_entry.get("sha256") if isinstance(old_entry, dict) else None
        old_semantics = old_entry.get("semantics", {}) if isinstance(old_entry, dict) else {}

        # Сравниваем: по хэшу или по семантике (если снимок был)
        if (old_hash and old_hash != sha256(new_text)) or old_semantics:
            d = diff(old_semantics, entry["semantics"])
            if has_changes(d):
                changed_reports.append(format_diff(name, label, d))

        filepath.write_text(new_text, encoding="utf-8")

    save(new_entries)

    # Git commit при изменениях
    git_msg = ""
    if changed_reports:
        git_msg = _git_commit_docs(changed_reports)

    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    err_str = f"\n⚠️  Не удалось скачать: {', '.join(errors)}" if errors else ""

    if not changed_reports:
        return True, f"✅ Документация [{now}] — изменений нет. Все {len(DOCS)} глав актуальны.{err_str}"

    report = "\n\n".join(changed_reports)
    return True, f"🔔 Документация [{now}] — обнаружены изменения!\n\n{report}\n\n📦 {git_msg}{err_str}"


def run_drift() -> tuple[bool, str]:
    """Запускает проверку дрейфа YAML → Pydantic → ORM."""
    from tools.drift.checker import run
    from tools.drift.reporter import format_report
    result = run()
    return result["clean"], format_report(result)


def _git_commit_docs(changed_reports: list[str]) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    names = []
    for r in changed_reports:
        line = r.splitlines()[0]
        if "(" in line and ")" in line:
            names.append(line.split("(")[1].rstrip(")"))
    msg = f"docs: update WB API specs [{date_str}]\n\nChanged: {', '.join(names)}"
    for cmd in [["git", "add", "docs/api/"], ["git", "commit", "-m", msg], ["git", "push", "origin", "main"]]:
        r = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0 and "nothing to commit" in (r.stdout + r.stderr):
            return "git: нечего коммитить"
    return "git: ok"


def main(commands: list[str] | None = None) -> int:
    """
    Точка входа. commands — список команд или None (полный проход).
    Возвращает 0 при успехе, 1 при ошибке.
    """
    if commands is None or commands == ["all"]:
        commands = ["migrate", "sync", "drift"]

    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"\n{'═' * 60}")
    print(f"  WB Collector Tools  [{now}]")
    print(f"{'═' * 60}")

    runners = {
        "migrate": ("🗄  Миграции БД",       run_migrate),
        "sync":    ("📡 Синхронизация YAML", run_sync),
        "drift":   ("🔍 Проверка дрейфа",   run_drift),
    }

    exit_code = 0
    for cmd in commands:
        if cmd not in runners:
            print(f"\n❌ Неизвестная команда: {cmd}")
            print(f"   Доступные: {', '.join(runners)}")
            return 1

        title, runner = runners[cmd]
        section(title)
        try:
            ok, message = runner()
            print(message)
            if not ok:
                exit_code = 1
        except Exception as e:
            print(f"❌ Ошибка при выполнении '{cmd}': {e}")
            exit_code = 1

    print(f"\n{'═' * 60}\n")
    return exit_code


if __name__ == "__main__":
    args = sys.argv[1:] or None
    sys.exit(main(args))
