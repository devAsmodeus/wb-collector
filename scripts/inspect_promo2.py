import yaml, json
with open('C:/Python/wb-collector/docs/api/08-promotion.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)

# server / host
for k, v in doc.items():
    if 'server' in k.lower() or 'host' in k.lower():
        print(k, v)

# normquery bodies
nq_paths = [
    '/adv/v0/normquery/stats', '/adv/v0/normquery/get-bids',
    '/adv/v0/normquery/bids', '/adv/v0/normquery/get-minus',
    '/adv/v0/normquery/set-minus', '/adv/v0/normquery/list',
    '/adv/v1/normquery/stats',
]
for path in nq_paths:
    for method, minfo in doc['paths'].get(path, {}).items():
        if not isinstance(minfo, dict):
            continue
        rb = minfo.get('requestBody', {})
        schema = rb.get('content', {}).get('application/json', {}).get('schema', {})
        ref = schema.get('$ref', '')
        stype = schema.get('type', '?')
        props = list(schema.get('properties', {}).keys())
        items_ref = schema.get('items', {}).get('$ref', '') or schema.get('items', {}).get('type', '')
        print(f'{method.upper()} {path}: type={stype} ref={ref} props={props} items={items_ref}')
        if ref:
            # resolve ref
            comp_name = ref.split('/')[-1]
            comp = doc.get('components', {}).get('schemas', {}).get(comp_name, {})
            for k, v in comp.get('properties', {}).items():
                t = v.get('type', v.get('$ref', '?'))
                print(f'    {k}: {t} — {str(v.get("description", ""))[:60]}')

# calendar params
print('\n=== Calendar params ===')
for path in ['/api/v1/calendar/promotions', '/api/v1/calendar/promotions/details',
             '/api/v1/calendar/promotions/nomenclatures', '/api/v1/calendar/promotions/upload']:
    for method, minfo in doc['paths'].get(path, {}).items():
        if not isinstance(minfo, dict):
            continue
        params = minfo.get('parameters', [])
        named = [p.get('name') for p in params if isinstance(p, dict) and p.get('name')]
        rb = minfo.get('requestBody', {})
        schema = rb.get('content', {}).get('application/json', {}).get('schema', {})
        props = list(schema.get('properties', {}).keys())
        print(f'{method.upper()} {path}: params={named} body_props={props}')
