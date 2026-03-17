import yaml
with open('C:/Python/wb-collector/docs/api/08-promotion.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)
print('server:', doc.get('servers', [{}])[0].get('url', 'none'))
paths_to_check = [
    '/adv/v0/normquery/stats', '/adv/v0/normquery/get-bids',
    '/adv/v0/normquery/bids', '/adv/v0/normquery/get-minus',
    '/adv/v0/normquery/set-minus', '/adv/v0/normquery/list',
    '/adv/v1/normquery/stats', '/adv/v2/supplier/nms', '/adv/v1/stats',
    '/api/v1/calendar/promotions', '/api/v1/calendar/promotions/details',
    '/api/v1/calendar/promotions/nomenclatures', '/api/v1/calendar/promotions/upload',
]
for path in paths_to_check:
    for method in ['post', 'get', 'delete', 'patch', 'put']:
        info = doc['paths'].get(path, {}).get(method, {})
        if not info:
            continue
        rb = info.get('requestBody', {})
        schema = rb.get('content', {}).get('application/json', {}).get('schema', {})
        props = schema.get('properties', {})
        if props:
            print(f'\n{method.upper()} {path}:')
            for k, v in props.items():
                t = v.get('type', v.get('$ref', '?'))
                d = str(v.get('description', ''))[:60]
                print(f'  {k}: {t} — {d}')
        elif schema.get('type') == 'array':
            item_type = schema.get('items', {}).get('type', 'object')
            print(f'\n{method.upper()} {path}: array of {item_type}')
        # also params
        params = info.get('parameters', [])
        if params:
            print(f'  params: {[p.get("name") for p in params if isinstance(p, dict)]}')
