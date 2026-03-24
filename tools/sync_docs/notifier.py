"""Форматирование отчёта об изменениях YAML."""


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

    if d["endpoints_removed"]:
        lines.append(f"  ❌ Удалённые эндпоинты ({len(d['endpoints_removed'])}):")
        for ep in d["endpoints_removed"][:5]:
            lines.append(f"      - {ep}")
        if len(d["endpoints_removed"]) > 5:
            lines.append(f"      ...ещё {len(d['endpoints_removed']) - 5}")

    if d.get("newly_deprecated"):
        lines.append(f"  ⚠️ Помечены устаревшими ({len(d['newly_deprecated'])}):")
        for ep in d["newly_deprecated"][:5]:
            lines.append(f"      ~ {ep}")
        if len(d["newly_deprecated"]) > 5:
            lines.append(f"      ...ещё {len(d['newly_deprecated']) - 5}")

    if d["methods_changed"]:
        lines.append(f"  🔄 Изменены HTTP-методы ({len(d['methods_changed'])}):")
        for m in d["methods_changed"][:3]:
            lines.append(f"      {m['path']}")
            if m["added"]:
                lines.append(f"        + {', '.join(m['added'])}")
            if m["removed"]:
                lines.append(f"        - {', '.join(m['removed'])}")

    if d["schemas_added"]:
        names = ", ".join(d["schemas_added"][:5])
        extra = f" (+{len(d['schemas_added'])-5})" if len(d["schemas_added"]) > 5 else ""
        lines.append(f"  📦 Новые схемы: {names}{extra}")

    if d["schemas_removed"]:
        lines.append(f"  🗑  Удалённые схемы: {', '.join(d['schemas_removed'][:5])}")

    if d["schemas_changed"]:
        lines.append(f"  🔧 Изменены схемы ({len(d['schemas_changed'])}):")
        for s in d["schemas_changed"][:5]:
            lines.append(f"      {s['schema']}")
            if s["fields_added"]:
                lines.append(f"        + поля: {', '.join(s['fields_added'])}")
            if s["fields_removed"]:
                lines.append(f"        - поля: {', '.join(s['fields_removed'])}")
        if len(d["schemas_changed"]) > 5:
            lines.append(f"      ...ещё {len(d['schemas_changed']) - 5}")

    return "\n".join(lines)


def format_report(changed: list[tuple[str, str, dict]], total: int, errors: list[str]) -> str:
    from datetime import datetime
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    err_str = f"\n⚠️ Не удалось проверить: {', '.join(errors)}" if errors else ""

    if not changed:
        return f"✅ WB API docs [{now}] — изменений нет. Все {total} глав актуальны.{err_str}"

    parts = [f"🔔 WB API docs [{now}] — обнаружены изменения!"]
    for name, label, d in changed:
        parts.append(format_diff(name, label, d))
    parts.append(err_str)
    return "\n\n".join(p for p in parts if p)
