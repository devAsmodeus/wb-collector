import yaml, sys
chapter = sys.argv[1]
names = sys.argv[2:]
with open(f'C:/Python/wb-collector/docs/api/{chapter}.yaml', encoding='utf-8') as f:
    doc = yaml.safe_load(f)
comps = doc.get('components', {}).get('schemas', {})
for name in names:
    s = comps.get(name, {})
    props = s.get('properties', {})
    print(f'=== {name} ===')
    for k, v in props.items():
        t = v.get('type', v.get('$ref', '?'))
        d = str(v.get('description', ''))[:70]
        print(f'  {k}: {t} — {d}')
    print()
