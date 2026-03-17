import yaml
with open('C:/Python/wb-collector/docs/api/07-orders-fbw.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)
servers = doc.get('servers', [])
for s in servers:
    print('server:', s.get('url', ''))
for path, methods in doc.get('paths', {}).items():
    for method, info in methods.items():
        if not isinstance(info, dict):
            continue
        resp = info.get('responses', {}).get('200', {})
        schema = resp.get('content', {}).get('application/json', {}).get('schema', {})
        props = schema.get('properties', {})
        if props:
            print(f'\nRESP {method.upper()} {path}:')
            for k, v in list(props.items())[:10]:
                t = v.get('type', '?')
                d = str(v.get('description', ''))[:70]
                print(f'  {k}: {t} — {d}')
        # also check array items
        items = schema.get('items', {})
        if items:
            item_props = items.get('properties', {})
            if item_props:
                print(f'\nRESP(array) {method.upper()} {path}:')
                for k, v in list(item_props.items())[:10]:
                    t = v.get('type', '?')
                    d = str(v.get('description', ''))[:70]
                    print(f'  {k}: {t} — {d}')
