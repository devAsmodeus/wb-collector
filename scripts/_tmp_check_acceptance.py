import yaml, json
with open('C:/Python/wb-collector/docs/api/07-orders-fbw.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)

# Найдем путь acceptance options
for path, methods in spec['paths'].items():
    if 'acceptance' in path or 'options' in path:
        print(f"Path: {path}")
        for m in methods:
            print(f"  method: {m}")

# Покажем схему OptionsResultModel
comps = spec.get('components', {}).get('schemas', {})
model = comps.get('models.OptionsResultModel', {})
# warehouses items props
warehouses = model.get('properties', {}).get('result', {}).get('items', {}).get('properties', {}).get('warehouses', {}).get('items', {}).get('properties', {})
print("\nwarehouse item fields:")
for k, v in warehouses.items():
    print(f"  {k}: {v.get('description','')[:80]}")
