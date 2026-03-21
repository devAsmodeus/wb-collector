"""Форматирование отчёта об изменениях YAML."""
from pathlib import Path

# Маппинг: имя схемы → файл Pydantic схемы (для подсказок)
SCHEMA_FILE_HINTS: dict[str, str] = {
    # FBW
    "models.Supply":        "src/schemas/fbw/supplies.py",
    "models.SupplyDetails": "src/schemas/fbw/supplies.py",
    "models.OptionsResultModel": "src/schemas/fbw/acceptance.py",
    # FBS
    "Supply":               "src/schemas/fbs/supplies.py",
    # DBS
    "OrderNew":             "src/schemas/dbs/orders.py",
    # Products
    "Card":                 "src/schemas/products/cards.py",
    "Price":                "src/schemas/products/prices.py",
}

# Маппинг: имя файла YAML → папка схем
YAML_TO_SCHEMA_DIR: dict[str, str] = {
    "01-general":         "src/schemas/general/",
    "02-products":        "src/schemas/products/",
    "03-orders-fbs":      "src/schemas/fbs/",
    "04-orders-dbw":      "src/schemas/dbw/",
    "05-orders-dbs":      "src/schemas/dbs/",
    "06-in-store-pickup": "src/schemas/pickup/",
    "07-orders-fbw":      "src/schemas/fbw/",
    "08-promotion":       "src/schemas/promotion/",
    "09-communications":  "src/schemas/communications/",
    "10-tariffs":         "src/schemas/tariffs/",
    "11-analytics":       "src/schemas/analytics/",
    "12-reports":         "src/schemas/reports/",
    "13-finances":        "src/schemas/finances/",
}


def format_diff(name: str, label: str, d: dict) -> str:
    lines = [f"📄 {label} ({name})"]

    if d["version_changed"]:
        lines.append(f"  • Версия: {d['old_version']} → {d['new_version']}")

    if d["endpoints_added"]:
        lines.append(f"  ✅ Новые эндпоинты ({len(d['endpoints_added'])}):")
        for ep in d["endpoints_added"][:5]:
            lines.append(f"      + {ep}")
        if len(d["endpoints_added"]) > 5:
            lines.append(f"      ...ещё {len(d['endpoints_added']) - 5}")
        schema_dir = YAML_TO_SCHEMA_DIR.get(name, "")
        if schema_dir:
            lines.append(f"  ⚠️  Добавьте контроллер/схему в: {schema_dir}")

    if d["endpoints_removed"]:
        lines.append(f"  ❌ Удалённые эндпоинты ({len(d['endpoints_removed'])}):")
        for ep in d["endpoints_removed"][:5]:
            lines.append(f"      - {ep}")

    if d["methods_changed"]:
        lines.append(f"  🔄 Изменены HTTP-методы ({len(d['methods_changed'])}):")
        for m in d["methods_changed"][:3]:
            lines.append(f"      {m['path']}")
            if m["added"]:
                lines.append(f"        + {', '.join(m['added'])}")
            if m["removed"]:
                lines.append(f"        - {', '.join(m['removed'])}")

    if d["schemas_added"]:
        lines.append(f"  📦 Новые схемы: {', '.join(d['schemas_added'][:5])}")
        if len(d["schemas_added"]) > 5:
            lines.append(f"      ...ещё {len(d['schemas_added']) - 5}")

    if d["schemas_removed"]:
        lines.append(f"  🗑  Удалённые схемы: {', '.join(d['schemas_removed'][:5])}")

    if d["schemas_changed"]:
        lines.append(f"  🔧 Изменены поля схем ({len(d['schemas_changed'])}):")
        for s in d["schemas_changed"][:8]:
            hint = SCHEMA_FILE_HINTS.get(s["schema"], YAML_TO_SCHEMA_DIR.get(name, ""))
            lines.append(f"      {s['schema']}  →  {hint}")
            if s["fields_added"]:
                lines.append(f"        + {', '.join(s['fields_added'])}")
            if s["fields_removed"]:
                lines.append(f"        - {', '.join(s['fields_removed'])}")
        if len(d["schemas_changed"]) > 8:
            lines.append(f"      ...ещё {len(d['schemas_changed']) - 8}")

    return "\n".join(lines)
