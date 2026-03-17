import yaml, sys

chapter = sys.argv[1] if len(sys.argv) > 1 else "03-orders-fbs"
with open(f'C:/Python/wb-collector/docs/api/{chapter}.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)

print(f"=== {data['info']['title']} ===")
print(f"Host: {data.get('servers', [{}])[0].get('url', 'N/A')}\n")

for path, methods in data['paths'].items():
    if not isinstance(methods, dict):
        continue
    for method, info in methods.items():
        if not isinstance(info, dict):
            continue
        summary = info.get('summary', '')
        params = [p.get('name', '?') for p in info.get('parameters', []) if isinstance(p, dict)]
        has_body = 'requestBody' in info
        resp_codes = list(info.get('responses', {}).keys())
        print(f"{method.upper():6} {path}")
        if summary: print(f"       summary: {summary}")
        if params:  print(f"       params:  {params}")
        if has_body: print(f"       body:    yes")
        print()
