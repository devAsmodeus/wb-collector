import yaml

with open('/app/docs/api/02-products.yaml') as f:
    doc = yaml.safe_load(f)

paths = doc.get('paths', {})
schemas = doc.get('components', {}).get('schemas', {})

print("=== ENDPOINTS ===")
for path, item in paths.items():
    for method in ['get', 'post', 'put', 'delete', 'patch']:
        op = item.get(method)
        if not op:
            continue
        servers = item.get('servers', doc.get('servers', [{}]))
        host = servers[0].get('url', '') if servers else ''
        params = [p.get('name') for p in op.get('parameters', [])]
        token_types = op.get('x-token-types', [])
        readonly = op.get('x-readonly-method', False)
        print(f"  {method.upper()} {host}{path}")
        print(f"    token={token_types} readonly={readonly} params={params}")

print("\n=== SCHEMAS (top-level) ===")
for name in sorted(schemas.keys()):
    s = schemas[name]
    props = list(s.get('properties', {}).keys())
    print(f"  {name}: {props[:8]}")
