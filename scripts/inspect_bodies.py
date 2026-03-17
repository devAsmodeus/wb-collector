import yaml, sys
chapter = sys.argv[1]
with open(f'C:/Python/wb-collector/docs/api/{chapter}.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)
for path, methods in doc.get('paths', {}).items():
    for method, info in methods.items():
        if not isinstance(info, dict): continue
        rb = info.get('requestBody')
        if rb:
            schema = rb.get('content', {}).get('application/json', {}).get('schema', {})
            props = schema.get('properties', {})
            if not props and 'items' in schema:
                props = schema['items'].get('properties', {})
            if props:
                print(f"\n{method.upper()} {path}:")
                for k, v in props.items():
                    t = v.get('type', '?')
                    d = v.get('description', '')[:80]
                    print(f"  {k}: {t} — {d}")
        # also responses
        resp = info.get('responses', {}).get('200', {})
        content = resp.get('content', {}).get('application/json', {}).get('schema', {})
        props = content.get('properties', {})
        if props:
            print(f"\n  RESPONSE {method.upper()} {path}:")
            for k, v in props.items():
                t = v.get('type', '?')
                d = v.get('description', '')[:80]
                print(f"    {k}: {t} — {d}")
