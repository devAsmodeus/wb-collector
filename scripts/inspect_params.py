import yaml, sys
chapter = sys.argv[1]
with open(f'C:/Python/wb-collector/docs/api/{chapter}.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)
for path, methods in doc.get('paths', {}).items():
    for method, info in methods.items():
        if not isinstance(info, dict): continue
        params = info.get('parameters', [])
        if params:
            print(f'{method.upper()} {path}:')
            for p in params:
                if isinstance(p, dict):
                    name = p.get('name', '?')
                    loc = p.get('in', '?')
                    desc = str(p.get('description', ''))[:70]
                    schema = p.get('schema', {})
                    typ = schema.get('type', '?')
                    print(f'  {name} ({loc}, {typ}) — {desc}')
