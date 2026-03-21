"""
Schema Drift Checker
=====================
Сравнивает поля схем WB API YAML с ORM моделями (SQLAlchemy).

Обнаруживает:
  - Поля которые есть в YAML, но отсутствуют в ORM (данные теряются)
  - Поля которые есть в ORM, но исчезли из YAML (возможный мусор)

Запуск: python scripts/check_schema_drift.py
"""

import sys
import os
from pathlib import Path

# Настраиваем путь для импорта src
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("WB_API_TOKEN", "dummy")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")

try:
    import yaml
except ImportError:
    os.system("pip install pyyaml -q")
    import yaml

# ─── Конфиг: какие YAML схемы сравниваем с какими ORM таблицами ──────────────

# Формат: (yaml_file, yaml_schema_name, orm_table_name, ignore_fields)
CHECKS = [
    # FBW Supplies
    ("07-orders-fbw", "models.Supply",        "fbw_supplies_ignored",  set()),
    ("07-orders-fbw", "models.SupplyDetails", "fbw_supplies_ignored",  set()),

    # FBS
    ("03-orders-fbs", "Supply",               "fbs_orders",
     {"createdAt","updatedAt","supplyId","name","closedAt","scanDt","isLargeCargo","isB2b"}),

    # Statistics (reports)
    # DBS orders
    ("05-orders-dbs", "Order",                "dbs_orders",
     {"deliveryMethod","offices","address","timeFrom","timeTo"}),
]

DOCS_DIR = ROOT / "docs" / "api"


# ─── Извлечение полей из YAML схемы ──────────────────────────────────────────

def get_yaml_schema_fields(yaml_file: str, schema_name: str) -> set[str]:
    """Возвращает set полей верхнего уровня YAML-схемы."""
    path = DOCS_DIR / f"{yaml_file}.yaml"
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    comps = spec.get("components", {}).get("schemas", {})
    schema = comps.get(schema_name, {})
    props = schema.get("properties", {})
    return set(props.keys())


# ─── Извлечение колонок из ORM моделей ───────────────────────────────────────

def get_orm_columns(table_name: str) -> set[str]:
    """Возвращает set имён колонок ORM модели по имени таблицы."""
    try:
        from sqlalchemy import inspect as sa_inspect
        from src.database import Base
        import src.models  # noqa

        for mapper in Base.registry.mappers:
            if mapper.persist_selectable.name == table_name:
                return {c.name for c in mapper.persist_selectable.columns}
    except Exception as e:
        print(f"  ⚠️  Не удалось загрузить ORM для {table_name}: {e}")
    return set()


# ─── Главная логика ───────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("Schema Drift Checker")
    print("=" * 60)

    # Специальный режим: проверяем manifest.json семантику vs ORM
    manifest_path = DOCS_DIR / "manifest.json"
    if manifest_path.exists():
        import json
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = manifest.get("files", [])
        if isinstance(files, list):
            print(f"\n📋 Семантический снимок манифеста:")
            for f in files:
                sem = f.get("semantics", {})
                ep_count  = len(sem.get("endpoints", {}))
                sch_count = len(sem.get("schemas", {}))
                print(f"  {f['file']:35} {ep_count:3} эндпоинтов, {sch_count:3} схем")

    print("\n" + "=" * 60)
    print("Детальная проверка ORM vs YAML")
    print("=" * 60)

    total_issues = 0

    for yaml_file, schema_name, table_name, ignore in CHECKS:
        yaml_fields = get_yaml_schema_fields(yaml_file, schema_name)
        if not yaml_fields:
            print(f"\n⚠️  {yaml_file} / {schema_name} — схема не найдена, пропускаем")
            continue

        orm_cols = get_orm_columns(table_name)

        # Поля которые есть в YAML но нет в ORM (риск потери данных)
        missing_in_orm = yaml_fields - orm_cols - ignore
        # Поля которые есть в ORM но нет в YAML (возможный мусор)
        extra_in_orm = orm_cols - yaml_fields - {"id", "fetched_at"} - ignore

        status = "✅" if not missing_in_orm and not extra_in_orm else "⚠️ "
        print(f"\n{status} {yaml_file} / {schema_name} → {table_name}")
        print(f"    YAML поля ({len(yaml_fields)}): {sorted(yaml_fields)[:8]}{'...' if len(yaml_fields)>8 else ''}")

        if orm_cols:
            print(f"    ORM колонки ({len(orm_cols)}): {sorted(orm_cols)[:8]}{'...' if len(orm_cols)>8 else ''}")
        else:
            print(f"    ORM: таблица не найдена или не загружена")

        if missing_in_orm:
            print(f"    ❌ Есть в YAML, нет в ORM: {sorted(missing_in_orm)}")
            total_issues += len(missing_in_orm)

        if extra_in_orm:
            print(f"    ℹ️  Есть в ORM, нет в YAML: {sorted(extra_in_orm)}")

    print("\n" + "=" * 60)
    if total_issues == 0:
        print("✅ Дрейфа не обнаружено")
    else:
        print(f"⚠️  Обнаружено {total_issues} полей без колонки в ORM — данные могут теряться!")
    print("=" * 60)


if __name__ == "__main__":
    run()
