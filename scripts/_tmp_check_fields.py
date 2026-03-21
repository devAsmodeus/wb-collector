import yaml, json

# FBW acceptance — ищем isBoxOnPallet и boxTypeID в схемах ответов
with open('C:/Python/wb-collector/docs/api/07-orders-fbw.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)

print("=== FBW acceptance options (POST /api/v3/acceptance/options) ===")
op = spec['paths'].get('/api/v3/acceptance/options', {}).get('post', {})
resp = op.get('responses', {}).get('200', {})
print(json.dumps(resp, ensure_ascii=False, indent=2)[:3000])

print("\n=== FBS orders — ищем isB2B ===")
with open('C:/Python/wb-collector/docs/api/03-orders-fbs.yaml', encoding='utf-8') as f:
    fbs_spec = yaml.safe_load(f)

comps = fbs_spec.get('components', {}).get('schemas', {})
for name, schema in comps.items():
    props = schema.get('properties', {})
    if 'isB2B' in props or 'isB2b' in props:
        key = 'isB2B' if 'isB2B' in props else 'isB2b'
        print(f"Schema: {name}, field: {key}")
        print(json.dumps(props.get(key), ensure_ascii=False))
