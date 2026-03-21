"""Форматирование отчёта дрейфа схем."""


def format_report(result: dict) -> str:
    lines = []

    pydantic_issues = result.get("pydantic", [])
    orm_issues      = result.get("orm", [])

    if result.get("clean"):
        return "✅ Drift check — расхождений нет. YAML, Pydantic и ORM синхронизированы."

    if pydantic_issues:
        lines.append(f"⚠️  YAML → Pydantic расхождения ({len(pydantic_issues)}):")
        for issue in pydantic_issues:
            lines.append(f"\n  {issue['source']}")
            lines.append(f"  → {issue['target']}")
            if issue["missing"]:
                lines.append(f"    ❌ Нет в Pydantic: {', '.join(issue['missing'])}")
                lines.append(f"       Добавьте поля в: {issue['target'].split(' / ')[0]}")
            if issue["extra"]:
                lines.append(f"    ℹ️  Лишние в Pydantic (нет в YAML): {', '.join(issue['extra'])}")

    if orm_issues:
        lines.append(f"\n⚠️  ORM предупреждения ({len(orm_issues)}):")
        for issue in orm_issues:
            warn = issue.get("warning", "")
            if warn:
                lines.append(f"  {issue['source']}: {warn}")

    if not lines:
        return "✅ Drift check — расхождений нет."

    return "\n".join(lines)
