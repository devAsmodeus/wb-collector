import yaml

with open('/app/docs/api/03-orders-fbs.yaml') as f:
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
        print(f"  {method.upper()} {host}{path} params={params}")

print("\n=== KEY SCHEMAS ===")
# Find order-related schemas
for name, s in schemas.items():
    if any(k in name.lower() for k in ['order', 'supply', 'sticker', 'package']):
        props = list(s.get('properties', {}).keys())
        print(f"  {name}: {props[:10]}")
