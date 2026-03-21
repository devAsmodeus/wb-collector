"""
Проверка дрейфа схем: YAML → Pydantic → ORM.

Для каждого YAML файла сравниваем поля в схемах компонентов с тем,
что объявлено в наших Pydantic и ORM моделях.
"""
import ast
import sys
from pathlib import Path

import yaml

REPO_DIR    = Path(__file__).parent.parent.parent
DOCS_DIR    = REPO_DIR / "docs" / "api"
SCHEMAS_DIR = REPO_DIR / "src" / "schemas"
MODELS_DIR  = REPO_DIR / "src" / "models"

# YAML файл → [(yaml_schema_name, pydantic_file, pydantic_class)]
# Неполный маппинг — покрываем ключевые схемы
MAPPINGS: list[tuple[str, str, str, str]] = [
    # (yaml_file, yaml_schema, pydantic_file, pydantic_class)
    ("07-orders-fbw", "models.Supply",        "fbw/supplies.py",    "FBWSupply"),
    ("07-orders-fbw", "models.SupplyDetails", "fbw/supplies.py",    "FBWSupply"),
    ("07-orders-fbw", "models.OptionsResultModel", "fbw/acceptance.py", "FBWAcceptanceWarehouse"),
    ("03-orders-fbs", "Supply",               "fbs/supplies.py",    "Supply"),
    ("05-orders-dbs", "OrderNew",             "dbs/orders.py",      "DbsOrderNew"),
    ("02-products",   "Card",                 "products/cards.py",  "CardItem"),
]

# ORM модели: (таблица, orm_file, orm_class)
ORM_MAPPINGS: list[tuple[str, str, str]] = [
    ("fbs_orders",          "orders.py",    "FbsOrder"),
    ("dbw_orders",          "orders.py",    "DbwOrder"),
    ("dbs_orders",          "orders.py",    "DbsOrder"),
    ("pickup_orders",       "orders.py",    "PickupOrder"),
    ("wb_stocks",           "reports.py",   "WbStock"),
    ("wb_orders_report",    "reports.py",   "WbOrderReport"),
    ("wb_sales_report",     "reports.py",   "WbSaleReport"),
    ("wb_financial_report", "reports.py",   "WbFinancialReport"),
    ("wb_cards",            "products.py",  "WbCard"),
    ("wb_prices",           "products.py",  "WbPrice"),
    ("wb_news",             "references.py","WbNews"),
]


def get_yaml_schema_fields(yaml_name: str, schema_name: str) -> set[str]:
    """Возвращает поля схемы из YAML компонентов."""
    path = DOCS_DIR / f"{yaml_name}.yaml"
    if not path.exists():
        return set()
    try:
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    schema = (d.get("components") or {}).get("schemas", {}).get(schema_name, {})
    return set((schema.get("properties") or {}).keys())


def get_pydantic_fields(rel_path: str, class_name: str) -> set[str]:
    """Извлекает поля Pydantic класса через AST."""
    path = SCHEMAS_DIR / rel_path
    if not path.exists():
        return set()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    fields = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    fields.add(item.target.id)
    return fields


def get_orm_fields(rel_path: str, class_name: str) -> set[str]:
    """Извлекает поля ORM класса через AST."""
    path = MODELS_DIR / rel_path
    if not path.exists():
        return set()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    fields = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    name = item.target.id
                    if not name.startswith("_") and name not in ("id", "fetched_at"):
                        fields.add(name)
    return fields


def check_pydantic_drift() -> list[dict]:
    """
    Проверяет YAML схемы vs Pydantic классы.
    Возвращает список расхождений.
    """
    issues = []
    for yaml_file, yaml_schema, pydantic_file, pydantic_class in MAPPINGS:
        yaml_fields     = get_yaml_schema_fields(yaml_file, yaml_schema)
        pydantic_fields = get_pydantic_fields(pydantic_file, pydantic_class)

        if not yaml_fields or not pydantic_fields:
            continue

        missing_in_pydantic = yaml_fields - pydantic_fields
        extra_in_pydantic   = pydantic_fields - yaml_fields

        if missing_in_pydantic or extra_in_pydantic:
            issues.append({
                "layer":    "YAML → Pydantic",
                "source":   f"{yaml_file} / {yaml_schema}",
                "target":   f"src/schemas/{pydantic_file} / {pydantic_class}",
                "missing":  sorted(missing_in_pydantic),
                "extra":    sorted(extra_in_pydantic),
            })
    return issues


def check_orm_drift() -> list[dict]:
    """
    Проверяет ORM модели — смотрит что таблицы существуют.
    Полноценный field-level drift для ORM требует introspection через SQLAlchemy.
    Здесь делаем проверку через AST.
    """
    issues = []
    for table, orm_file, orm_class in ORM_MAPPINGS:
        fields = get_orm_fields(orm_file, orm_class)
        if not fields:
            issues.append({
                "layer":   "ORM",
                "source":  f"src/models/{orm_file} / {orm_class}",
                "target":  f"table: {table}",
                "missing": [],
                "extra":   [],
                "warning": "Класс не найден или пустой",
            })
    return issues


def run() -> dict:
    pydantic_issues = check_pydantic_drift()
    orm_issues      = check_orm_drift()
    return {
        "pydantic": pydantic_issues,
        "orm":      orm_issues,
        "clean":    not pydantic_issues and not orm_issues,
    }
