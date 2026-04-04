import yaml

with open('/app/docs/api/05-orders-dbs.yaml') as f:
    spec = yaml.safe_load(f)

schemas = spec.get('components', {}).get('schemas', {})
print("Schemas:", list(schemas.keys()))
for name, s in schemas.items():
    props = s.get('properties', {})
    if props and len(props) > 4:
        print(f"\n--- {name} ---")
        for k, v in props.items():
            t = v.get('type', v.get('$ref', '?'))
            print(f"  {k}: {t}")

# Also check paths
print("\n=== Paths ===")
for path, methods in spec.get('paths', {}).items():
    for method in ['get', 'post', 'put', 'patch', 'delete']:
        if method in methods:
            print(f"  {method.upper()} {path}")
