import yaml, json

# Проверяем OptionsResultModel детально
with open('C:/Python/wb-collector/docs/api/07-orders-fbw.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)

comps = spec.get('components', {}).get('schemas', {})
model = comps.get('models.OptionsResultModel', {})
print("=== models.OptionsResultModel ===")
print(json.dumps(model, ensure_ascii=False, indent=2)[:3000])

# FBS Supply schema (для isB2b)
print("\n=== FBS Supply schema ===")
with open('C:/Python/wb-collector/docs/api/03-orders-fbs.yaml', encoding='utf-8') as f:
    fbs = yaml.safe_load(f)
fbs_comps = fbs.get('components', {}).get('schemas', {})
supply = fbs_comps.get('Supply', {})
props = supply.get('properties', {})
b2b = props.get('isB2b') or props.get('isB2B')
print(f"isB2b field: {json.dumps(b2b, ensure_ascii=False)}")

# Где в FBS используется Supply с isB2b
print("\n=== FBS paths using Supply ===")
for path, methods in fbs.get('paths', {}).items():
    for method, op in methods.items():
        if method not in ('get','post'):
            continue
        text = json.dumps(op, ensure_ascii=False)
        if 'Supply' in text:
            print(f"  {method.upper()} {path}")
