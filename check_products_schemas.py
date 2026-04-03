import yaml

with open('/app/docs/api/02-products.yaml') as f:
    doc = yaml.safe_load(f)

schemas = doc.get('components', {}).get('schemas', {})
paths = doc.get('paths', {})

def print_schema(name, schemas, indent=0):
    s = schemas.get(name, {})
    if not s:
        print(f"{'  '*indent}[{name}] NOT FOUND")
        return
    prefix = '  ' * indent
    required = s.get('required', [])
    for field, info in s.get('properties', {}).items():
        ft = info.get('type', '?')
        ref = info.get('$ref', '')
        req = '*' if field in required else ''
        fmt = f" ({info['format']})" if 'format' in info else ''
        if ref:
            ref_name = ref.split('/')[-1]
            print(f"{prefix}  {field}{req}: -> {ref_name}")
        elif ft == 'array':
            item = info.get('items', {})
            item_ref = item.get('$ref', '')
            print(f"{prefix}  {field}{req}: array of {item_ref.split('/')[-1] if item_ref else item.get('type','?')}")
        else:
            print(f"{prefix}  {field}{req}: {ft}{fmt}")

# Карточки
print("=== cards/list response ===")
cards_resp = paths.get('/content/v2/get/cards/list', {}).get('post', {}).get('responses', {}).get('200', {})
cards_schema = cards_resp.get('content', {}).get('application/json', {}).get('schema', {})
print(yaml.dump(cards_schema, allow_unicode=True, default_flow_style=False)[:2000])

# Цены
print("=== GoodsList schema ===")
print_schema('GoodsList', schemas)

print("=== Warehouse schema ===")
print_schema('Warehouse', schemas)

print("=== Office schema ===")
print_schema('Office', schemas)

# Tags
tags_resp = paths.get('/content/v2/tags', {}).get('get', {}).get('responses', {}).get('200', {})
tags_schema = tags_resp.get('content', {}).get('application/json', {}).get('schema', {})
print("=== tags response ===")
print(yaml.dump(tags_schema, allow_unicode=True, default_flow_style=False)[:1000])
