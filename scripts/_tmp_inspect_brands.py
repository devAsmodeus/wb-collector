import yaml, json
with open('C:/Python/wb-collector/docs/api/02-products.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)
comps = spec.get('components', {}).get('schemas', {})
br = comps.get('BrandsResponse', {})
print(json.dumps(br, ensure_ascii=False, indent=2)[:2000])
