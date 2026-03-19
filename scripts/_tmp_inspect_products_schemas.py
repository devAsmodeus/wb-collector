import yaml, json

endpoints = [
    '/content/v2/object/parent/all',
    '/content/v2/object/all',
    '/content/v2/object/charcs/{subjectId}',
    '/content/v2/directory/colors',
    '/content/v2/directory/kinds',
    '/content/v2/directory/countries',
    '/content/v2/directory/seasons',
    '/content/v2/directory/vat',
    '/content/v2/directory/tnved',
    '/api/content/v1/brands',
]

with open('C:/Python/wb-collector/docs/api/02-products.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)

for ep in endpoints:
    op = spec['paths'].get(ep, {}).get('get', {})
    schema = op.get('responses', {}).get('200', {}).get('content', {})
    for ct, v in schema.items():
        props = v.get('schema', {}).get('properties', {})
        # ищем items в data/result
        for key in ('data', 'result', 'error'):
            if key in props:
                items = props[key].get('items', {}).get('properties', {})
                if items:
                    print(f"\n{ep}")
                    for fname, fval in items.items():
                        print(f"  {fname}: {fval.get('type','?')} — {fval.get('description','')[:60]}")
                    break
        else:
            # flat response
            flat = v.get('schema', {}).get('properties', {})
            if flat and ep not in ['/content/v2/object/parent/all', '/content/v2/object/all']:
                print(f"\n{ep} (flat)")
                for fname, fval in list(flat.items())[:8]:
                    print(f"  {fname}: {fval.get('type','?')} — {fval.get('description','')[:60]}")
