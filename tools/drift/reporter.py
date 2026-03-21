"""Форматирование отчёта о дрейфе схем."""


def format_report(result: dict) -> str:
    issues = result["issues"]
    lines  = [
        f"🔍 Drift check: {result['yaml_schemas']} YAML схем | "
        f"{result['pydantic_classes']} Pydantic классов | "
        f"{result['orm_classes']} ORM моделей"
    ]

    if not issues:
        lines.append("✅ Дрейфа нет — все слои синхронизированы.")
        return "\n".join(lines)

    lines.append(f"⚠️  Найдено расхождений: {len(issues)}\n")

    yaml_issues     = [i for i in issues if i["layer"] == "yaml→pydantic"]
    pydantic_issues = [i for i in issues if i["layer"] == "pydantic→orm"]

    if yaml_issues:
        lines.append("── YAML → Pydantic ──────────────────────────")
        for issue in yaml_issues:
            lines.append(f"  {issue['yaml_schema']} → {issue['pydantic_class']}")
            if issue["missing_in_code"]:
                lines.append(f"    ❌ нет в Pydantic: {', '.join(issue['missing_in_code'])}")
            if issue["extra_in_code"]:
                lines.append(f"    ➕ лишние в Pydantic: {', '.join(issue['extra_in_code'])}")

    if pydantic_issues:
        lines.append("\n── Pydantic → ORM ───────────────────────────")
        for issue in pydantic_issues:
            lines.append(f"  {issue['pydantic_class']} → {issue['orm_class']}")
            if issue["missing_in_orm"]:
                lines.append(f"    ❌ нет в ORM: {', '.join(issue['missing_in_orm'])}")

    return "\n".join(lines)
