import yaml, json

with open('C:/Python/wb-collector/docs/api/07-orders-fbw.yaml', encoding='utf-8') as f:
    fbw = yaml.safe_load(f)

comps = fbw.get('components', {}).get('schemas', {})

# Найдём OptionsResultModel и его вложенные схемы
def resolve_ref(ref, comps):
    name = ref.split('/')[-1]
    return comps.get(name, {}), name

def print_schema(name, schema, comps, depth=0):
    indent = "  " * depth
    props = schema.get('properties', {})
    if props:
        print(f"{indent}Schema '{name}':")
        for k, v in props.items():
            ref = v.get('$ref', '')
            if ref:
                nested, nested_name = resolve_ref(ref, comps)
                print(f"{indent}  {k}: -> {nested_name}")
            else:
                print(f"{indent}  {k}: {v.get('type','?')} — {v.get('description','')[:50]}")
    items = schema.get('items', {})
    if items:
        ref = items.get('$ref', '')
        if ref:
            nested, nested_name = resolve_ref(ref, comps)
            print(f"{indent}  (array items) -> {nested_name}")
            print_schema(nested_name, nested, comps, depth+1)

s, _ = resolve_ref('#/components/schemas/models.OptionsResultModel', comps)
print_schema('models.OptionsResultModel', s, comps)
