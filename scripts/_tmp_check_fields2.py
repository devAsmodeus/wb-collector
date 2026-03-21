import yaml, json

with open('C:/Python/wb-collector/docs/api/07-orders-fbw.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)

# Смотрим все пути с isBoxOnPallet
print("=== Пути где есть isBoxOnPallet/boxTypeID ===")
for path, methods in spec.get('paths', {}).items():
    for method, op in methods.items():
        if method not in ('get','post','put','patch','delete'):
            continue
        text = json.dumps(op, ensure_ascii=False)
        if 'isBoxOnPallet' in text or 'boxTypeID' in text:
            print(f"  {method.upper()} {path}")

# Смотрим компоненты где есть эти поля
print("\n=== Компоненты/схемы с isBoxOnPallet ===")
comps = spec.get('components', {}).get('schemas', {})
for name, schema in comps.items():
    s = json.dumps(schema, ensure_ascii=False)
    if 'isBoxOnPallet' in s or 'boxTypeID' in s:
        props = schema.get('properties', {})
        print(f"Schema: {name}")
        if 'isBoxOnPallet' in props:
            print(f"  isBoxOnPallet: {props['isBoxOnPallet'].get('description','')}")
        if 'boxTypeID' in props:
            print(f"  boxTypeID: {props['boxTypeID'].get('description','')}")

# FBS — ищем isB2B в путях
print("\n=== FBS пути с isB2B/isB2b ===")
with open('C:/Python/wb-collector/docs/api/03-orders-fbs.yaml', encoding='utf-8') as f:
    fbs = yaml.safe_load(f)
for path, methods in fbs.get('paths', {}).items():
    for method, op in methods.items():
        if method not in ('get','post','put','patch','delete'):
            continue
        text = json.dumps(op, ensure_ascii=False)
        if 'isB2B' in text or 'isB2b' in text:
            print(f"  {method.upper()} {path}")
