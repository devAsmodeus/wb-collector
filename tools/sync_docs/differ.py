"""Семантический diff двух OpenAPI YAML файлов."""
try:
    import yaml
except ImportError:
    import os; os.system("pip install pyyaml -q")
    import yaml


def _extract_fields(schema: dict, depth: int = 0) -> list[str]:
    """Извлечь поля из схемы (до 2 уровней)."""
    if depth > 2 or not isinstance(schema, dict):
        return []
    fields = []
    props = schema.get("properties", {})
    if isinstance(props, dict):
        fields.extend(props.keys())
        if depth < 1:
            for v in props.values():
                if isinstance(v, dict):
                    fields.extend(_extract_fields(v, depth + 1))
    items = schema.get("items", {})
    if isinstance(items, dict) and depth < 1:
        fields.extend(_extract_fields(items, depth + 1))
    return fields


def extract_semantics(text: str) -> dict:
    """Извлечь семантику спека из YAML текста."""
    try:
        d = yaml.safe_load(text)
    except Exception:
        return {}

    global_servers = [s.get("url", "") for s in (d.get("servers") or [])]

    endpoints = {}
    deprecated = {}
    endpoint_servers = {}

    for path, methods in (d.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        http = [m for m in methods if m in ("get", "post", "put", "patch", "delete")]
        if http:
            endpoints[path] = sorted(http)
            # Помечаем deprecated если хоть один метод deprecated
            for m in http:
                if methods.get(m, {}).get("deprecated") is True:
                    deprecated[path] = True
                    break
            # Серверы: operation level > path item level > global level
            method_obj = methods.get(http[0], {})
            op_servers = [s.get("url", "") for s in (method_obj.get("servers") or [])]
            path_servers = [s.get("url", "") for s in (methods.get("servers") or [])]
            effective_servers = sorted(op_servers or path_servers or global_servers)
            if effective_servers:
                endpoint_servers[path] = effective_servers

    schemas = {}
    for name, schema in ((d.get("components") or {}).get("schemas", {}) or {}).items():
        if isinstance(schema, dict):
            schemas[name] = sorted(set(_extract_fields(schema)))

    return {
        "version":          (d.get("info") or {}).get("version", ""),
        "endpoints":        endpoints,
        "deprecated":       deprecated,
        "schemas":          schemas,
        "endpoint_servers": endpoint_servers,
    }


def diff(old: dict, new: dict) -> dict:
    """Сравнить две семантики спека."""
    old_eps = set(old.get("endpoints", {}).keys())
    new_eps = set(new.get("endpoints", {}).keys())
    old_sch = old.get("schemas", {})
    new_sch = new.get("schemas", {})

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

    changed_schemas = []
    for name in set(old_sch) & set(new_sch):
        added   = sorted(set(new_sch[name]) - set(old_sch[name]))
        removed = sorted(set(old_sch[name]) - set(new_sch[name]))
        if added or removed:
            changed_schemas.append({
                "schema":         name,
                "fields_added":   added,
                "fields_removed": removed,
            })

    # Пути которые стали deprecated (не были раньше)
    old_dep = set(old.get("deprecated", {}).keys())
    new_dep = set(new.get("deprecated", {}).keys())
    newly_deprecated = sorted(new_dep - old_dep)

    # Изменения серверов для endpoint'ов
    old_srv = old.get("endpoint_servers", {})
    new_srv = new.get("endpoint_servers", {})
    server_changes = []
    for path in set(list(old_srv.keys()) + list(new_srv.keys())):
        o = old_srv.get(path, [])
        n = new_srv.get(path, [])
        if o != n:
            server_changes.append({"path": path, "old_servers": o, "new_servers": n})

    return {
        "version_changed":   old.get("version") != new.get("version"),
        "old_version":       old.get("version"),
        "new_version":       new.get("version"),
        "endpoints_added":   sorted(new_eps - old_eps),
        "endpoints_removed": sorted(old_eps - new_eps),
        "methods_changed":   changed_methods,
        "newly_deprecated":  newly_deprecated,
        "schemas_added":     sorted(set(new_sch) - set(old_sch)),
        "schemas_removed":   sorted(set(old_sch) - set(new_sch)),
        "schemas_changed":   changed_schemas,
        "server_changes":    server_changes,
    }


def has_changes(d: dict) -> bool:
    return bool(
        d["version_changed"] or d["endpoints_added"] or d["endpoints_removed"] or
        d["methods_changed"] or d["newly_deprecated"] or
        d["schemas_added"] or d["schemas_removed"] or d["schemas_changed"] or
        d.get("server_changes")
    )
