import yaml

for fname, label in [('12-reports.yaml', '12'), ('13-finances.yaml', '13')]:
    with open(f'C:/Python/wb-collector/docs/api/{fname}', encoding='utf-8') as f:
        doc = yaml.safe_load(f)
    print(f'\n=== {fname} ===')
    for path, methods in doc.get('paths', {}).items():
        for method, info in methods.items():
            if not isinstance(info, dict): continue
            params = [p.get('name') for p in info.get('parameters', []) if isinstance(p, dict) and p.get('name')]
            has_body = bool(info.get('requestBody'))
            print(f'  {method.upper():6} {path}  params={params}  body={has_body}')
