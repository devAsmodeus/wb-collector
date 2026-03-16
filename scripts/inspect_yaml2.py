"""Полный дамп всех эндпоинтов с параметрами и схемами ответов."""
import yaml, json, sys

file = sys.argv[1]

with open(file, encoding="utf-8") as f:
    d = yaml.safe_load(f)

def resolve(ref_str, doc):
    parts = ref_str.lstrip("#/").split("/")
    node = doc
    for p in parts:
        node = node.get(p, {})
    return node

def flatten_schema(schema, doc, depth=0):
    if depth > 3:
        return {}
    if "$ref" in schema:
        return flatten_schema(resolve(schema["$ref"], doc), doc, depth)
    result = {}
    props = schema.get("properties", {})
    for k, v in props.items():
        if "$ref" in v:
            result[k] = flatten_schema(v, doc, depth+1)
        elif v.get("type") == "array":
            items = v.get("items", {})
            result[k] = [flatten_schema(items, doc, depth+1) if "$ref" in items or "properties" in items else items.get("type","?")]
        else:
            result[k] = {"type": v.get("type","?"), "desc": v.get("description","")}
    return result

for path, methods in d["paths"].items():
    for method, spec in methods.items():
        if method not in ("get","post","put","patch","delete"):
            continue
        print(f"\n{'='*60}")
        print(f"{method.upper()} {path}")
        print(f"Summary: {spec.get('summary','')}")

        params = spec.get("parameters", [])
        if params:
            print("Parameters:")
            for p in params:
                req = "required" if p.get("required") else "optional"
                typ = p.get("schema",{}).get("type","?")
                print(f"  {p['name']} ({typ}, {req}): {p.get('description','')}")

        body = spec.get("requestBody",{})
        if body:
            content = body.get("content",{}).get("application/json",{})
            schema = content.get("schema",{})
            flat = flatten_schema(schema, d)
            if flat:
                print(f"Request body:")
                print(f"  {json.dumps(flat, ensure_ascii=False, indent=4)}")

        resp = spec.get("responses",{}).get("200",{})
        content = resp.get("content",{}).get("application/json",{})
        schema = content.get("schema",{})
        if schema:
            flat = flatten_schema(schema, d)
            if flat:
                print(f"Response 200:")
                print(f"  {json.dumps(flat, ensure_ascii=False, indent=4)}")
