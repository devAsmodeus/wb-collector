import yaml, json, sys

file = sys.argv[1] if len(sys.argv) > 1 else "C:/Python/wb-collector/docs/api/01-general.yaml"
path_filter = sys.argv[2] if len(sys.argv) > 2 else "/api/v1/seller-info"

with open(file, encoding="utf-8") as f:
    d = yaml.safe_load(f)

def resolve_ref(ref_str, doc):
    parts = ref_str.lstrip("#/").split("/")
    node = doc
    for p in parts:
        node = node[p]
    return node

def show_schema(schema, doc, indent=0):
    if "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        resolved = resolve_ref(schema["$ref"], doc)
        print(" " * indent + f"$ref: {name}")
        show_schema(resolved, doc, indent)
        return
    props = schema.get("properties", {})
    for k, v in props.items():
        typ = v.get("type", v.get("$ref", "?").split("/")[-1] if "$ref" in v else "?")
        desc = v.get("description", "")
        print(" " * indent + f"  {k}: {typ}  # {desc}")

for path, methods in d["paths"].items():
    if path_filter and path_filter not in path:
        continue
    for method, spec in methods.items():
        if method not in ("get", "post", "put", "patch", "delete"):
            continue
        print(f"\n{'='*60}")
        print(f"{method.upper()} {path}")
        print(f"Summary: {spec.get('summary','')}")
        
        # Parameters
        params = spec.get("parameters", [])
        if params:
            print("Parameters:")
            for p in params:
                print(f"  {p['name']} ({p.get('in','')}, {'required' if p.get('required') else 'optional'}): {p.get('description','')}")
        
        # Response 200
        resp = spec.get("responses", {}).get("200", {})
        content = resp.get("content", {}).get("application/json", {})
        schema = content.get("schema", {})
        if schema:
            print("Response 200 schema:")
            show_schema(schema, d, 0)
