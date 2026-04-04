import yaml

with open('/app/docs/api/03-orders-fbs.yaml') as f:
    doc = yaml.safe_load(f)

schemas = doc.get('components', {}).get('schemas', {})

def print_schema(name, depth=0, visited=None):
    if visited is None:
        visited = set()
    if name in visited or depth > 3:
        return
    visited.add(name)
    s = schemas.get(name, {})
    prefix = '  ' * depth
    req = s.get('required', [])
    for field, info in s.get('properties', {}).items():
        ft = info.get('type', '?')
        ref = info.get('$ref', '')
        r = '*' if field in req else ''
        fmt = f" ({info.get('format','')})" if info.get('format') else ''
        if ref:
            ref_name = ref.split('/')[-1]
            print(f"{prefix}  {field}{r}: → {ref_name}")
            print_schema(ref_name, depth+1, visited)
        elif ft == 'array':
            item = info.get('items', {})
            ir = item.get('$ref', '')
            itype = ir.split('/')[-1] if ir else item.get('type', '?')
            print(f"{prefix}  {field}{r}: [{itype}]")
        else:
            print(f"{prefix}  {field}{r}: {ft}{fmt}")

print("=== Order schema ===")
print_schema('Order')

print("\n=== OrderNew schema ===")
print_schema('OrderNew')

print("\n=== Supply schema ===")
print_schema('Supply')
