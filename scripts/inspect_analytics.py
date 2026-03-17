import yaml

with open('C:/Python/wb-collector/docs/api/11-analytics.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)

for path, methods in doc.get('paths', {}).items():
    for method, info in methods.items():
        if not isinstance(info, dict):
            continue
        params = info.get('parameters', [])
        param_names = [p.get('name') for p in params if isinstance(p, dict) and p.get('name')]
        rb = info.get('requestBody', {})
        has_body = bool(rb)
        print(f'{method.upper():6} {path}  params={param_names}  body={has_body}')
