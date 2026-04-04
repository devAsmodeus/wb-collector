import yaml, glob

files = glob.glob('/app/docs/api/06*.yaml') + glob.glob('/app/docs/api/*pickup*.yaml')
print('Files:', files)
if not files:
    import os
    print('All YAMLs:', sorted(os.listdir('/app/docs/api')))
    exit()

with open(files[0]) as f:
    spec = yaml.safe_load(f)

schemas = spec.get('components', {}).get('schemas', {})
print("Schemas:", list(schemas.keys()))
for name, s in schemas.items():
    props = s.get('properties', {})
    if props and len(props) > 3:
        print(f"\n--- {name} ---")
        for k, v in props.items():
            t = v.get('type', v.get('$ref', '?'))
            print(f"  {k}: {t}")

print("\n=== Paths ===")
for path, methods in spec.get('paths', {}).items():
    for method in ['get', 'post', 'put', 'patch', 'delete']:
        if method in methods:
            print(f"  {method.upper()} {path}")
