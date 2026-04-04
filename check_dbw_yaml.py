import yaml, os

yaml_file = '/app/docs/api/04-orders-dbw.yaml'
if not os.path.exists(yaml_file):
    print(f"NOT FOUND: {yaml_file}")
    import glob
    print("Available:", glob.glob('/app/docs/api/0*.yaml'))
else:
    with open(yaml_file) as f:
        spec = yaml.safe_load(f)
    schemas = spec.get('components', {}).get('schemas', {})
    print("Schemas:", list(schemas.keys()))
    for name, s in schemas.items():
        props = s.get('properties', {})
        if props and len(props) > 4:
            print(f"\n--- {name} ---")
            for k, v in props.items():
                t = v.get('type', v.get('$ref', '?'))
                print(f"  {k}: {t}")
