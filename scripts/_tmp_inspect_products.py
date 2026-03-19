import yaml
with open('C:/Python/wb-collector/docs/api/02-products.yaml', encoding='utf-8') as f:
    spec = yaml.safe_load(f)
for path, methods in spec.get('paths', {}).items():
    for method, op in methods.items():
        if method in ('get','post','put','patch','delete'):
            tags = op.get('tags', [])
            summary = op.get('summary', '')[:60]
            print(f"{method.upper():6} {path:60} [{', '.join(tags)}]")
