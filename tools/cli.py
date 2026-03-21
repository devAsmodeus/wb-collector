"""
WB Collector Tools
==================
Единая точка запуска всех инструментов.

Использование:
    python -m tools             # полный проход (migrate → sync_docs → drift)
    python -m tools migrate     # только миграции
    python -m tools sync        # только синхронизация документации
    python -m tools drift       # только проверка дрейфа схем
"""
import sys
from datetime import datetime


def run_migrate() -> dict:
    from tools.migrate.runner import run_migrations, get_current_revision
    print("─" * 50)
    print("⚙️  [1/3] Миграции БД")
    print("─" * 50)
    result  = run_migrations()
    revision = get_current_revision()
    icon    = "✅" if result["success"] else "❌"
    print(f"{icon} Статус:   {result['status']}")
    print(f"   Ревизия: {revision or 'неизвестна'}")
    if result["output"] and result["status"] not in ("up_to_date",):
        print(f"   Вывод:   {result['output'][:200]}")
    return result


def run_sync() -> dict:
    from tools.sync_docs.runner import run
    print("\n" + "─" * 50)
    print("📡 [2/3] Синхронизация WB API документации")
    print("─" * 50)
    result = run()
    print(result["report"])
    return result


def run_drift() -> dict:
    from tools.drift.checker  import check_drift
    from tools.drift.reporter import format_report
    print("\n" + "─" * 50)
    print("🔍 [3/3] Проверка дрейфа схем (YAML → Pydantic → ORM)")
    print("─" * 50)
    result = check_drift()
    print(format_report(result))
    return result


def main(command: str = "all") -> int:
    start = datetime.now()
    print(f"\n{'═' * 50}")
    print(f"  WB Collector Tools — {start.strftime('%d.%m.%Y %H:%M')}")
    print(f"{'═' * 50}")

    results = {}

    if command in ("all", "migrate"):
        results["migrate"] = run_migrate()

    if command in ("all", "sync"):
        results["sync"] = run_sync()

    if command in ("all", "drift"):
        results["drift"] = run_drift()

    elapsed = (datetime.now() - start).total_seconds()
    print(f"\n{'─' * 50}")
    print(f"⏱  Завершено за {elapsed:.1f}с")

    # Возвращаем код ошибки если миграция упала
    if "migrate" in results and not results["migrate"].get("success"):
        return 1
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    sys.exit(main(cmd))
