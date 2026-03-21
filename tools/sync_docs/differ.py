"""Семантический diff двух снимков YAML."""


def diff(old: dict, new: dict) -> dict:
    """Сравнивает два семантических снимка."""
    old_eps = set(old.get("endpoints", {}).keys())
    new_eps = set(new.get("endpoints", {}).keys())

    old_schemas = old.get("schemas", {})
    new_schemas = new.get("schemas", {})

    # Изменения HTTP методов на существующих путях
    changed_methods = []
    for path in old_eps & new_eps:
        om = set(old["endpoints"][path])
        nm = set(new["endpoints"][path])
        if om != nm:
            changed_methods.append({
                "path":    path,
                "added":   sorted(nm - om),
                "removed": sorted(om - nm),
            })

    # Изменения полей в существующих схемах
    changed_schemas = []
    for name in set(old_schemas) & set(new_schemas):
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


def has_changes(d: dict) -> bool:
    return bool(
        d["version_changed"] or
        d["endpoints_added"] or
        d["endpoints_removed"] or
        d["methods_changed"] or
        d["schemas_added"] or
        d["schemas_removed"] or
        d["schemas_changed"]
    )
