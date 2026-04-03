import yaml, json

with open('/app/docs/api/01-general.yaml') as f:
    doc = yaml.safe_load(f)

schemas = doc.get('components', {}).get('schemas', {})

# Разворачиваем getUsersResponse полностью
def resolve_ref(ref, schemas):
    name = ref.split('/')[-1]
    return schemas.get(name, {})

def print_schema(name, schemas, indent=0):
    s = schemas.get(name, {})
    prefix = '  ' * indent
    t = s.get('type', '?')
    print(f"{prefix}[{name}] type={t}")
    for field, info in s.get('properties', {}).items():
        ft = info.get('type', '?')
        ref = info.get('$ref', '')
        req = ' *' if field in s.get('required', []) else ''
        if ref:
            ref_name = ref.split('/')[-1]
            print(f"{prefix}  {field}{req}: -> {ref_name}")
            print_schema(ref_name, schemas, indent+2)
        elif ft == 'array':
            item = info.get('items', {})
            item_ref = item.get('$ref', '')
            item_type = item.get('type', '?')
            if item_ref:
                item_name = item_ref.split('/')[-1]
                print(f"{prefix}  {field}{req}: array of -> {item_name}")
                print_schema(item_name, schemas, indent+2)
            else:
                print(f"{prefix}  {field}{req}: array of {item_type}")
                for k, v in item.get('properties', {}).items():
                    print(f"{prefix}    {k}: {v.get('type','?')}")
        else:
            fmt = f" ({info['format']})" if 'format' in info else ''
            print(f"{prefix}  {field}{req}: {ft}{fmt}")

print_schema('getUsersResponse', schemas)
