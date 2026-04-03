import yaml

with open('/app/docs/api/01-general.yaml') as f:
    doc = yaml.safe_load(f)

schemas = doc.get('components', {}).get('schemas', {})

targets = ['SellerInfo', 'NewsItem', 'NewsResponse', 'SupplierRatingModel', 'SubscriptionsJamInfo', 'User', 'UserInfo', 'UserAccess']
for name in targets:
    if name in schemas:
        s = schemas[name]
        props = s.get('properties', {})
        required = s.get('required', [])
        print(f'=== {name} ===')
        for field, info in props.items():
            t = info.get('type', str(info.get('$ref', '?')))
            req = ' [required]' if field in required else ''
            fmt = f" ({info['format']})" if 'format' in info else ''
            print(f'  {field}{req}: {t}{fmt}')
        print()
    else:
        print(f'=== {name} — NOT FOUND ===\n')

# Также смотрим news endpoint response schema
paths = doc.get('paths', {})
news_path = paths.get('/api/communications/v2/news', {})
news_op = news_path.get('get', {})
resp = news_op.get('responses', {}).get('200', {})
content = resp.get('content', {}).get('application/json', {})
schema = content.get('schema', {})
print('=== NEWS response schema ===')
print(yaml.dump(schema, allow_unicode=True, default_flow_style=False))

seller_path = paths.get('/api/v1/seller-info', {})
seller_op = seller_path.get('get', {})
resp2 = seller_op.get('responses', {}).get('200', {})
content2 = resp2.get('content', {}).get('application/json', {})
schema2 = content2.get('schema', {})
print('=== SELLER-INFO response schema ===')
print(yaml.dump(schema2, allow_unicode=True, default_flow_style=False))
