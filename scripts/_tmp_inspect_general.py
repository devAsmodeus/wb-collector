import yaml
with open('C:/Python/wb-collector/docs/api/01-general.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)
for path, methods in spec.get('paths', {}).items():
    for method, op in methods.items():
        if method in ('get','post','put','patch','delete'):
            summary = op.get('summary', '')[:60]
            tags = op.get('tags', [])
            print(f"{method.upper():6} {path:55} [{', '.join(tags)}] {summary}")
