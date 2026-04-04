import re

# 1. Fix sync service: get_max_date -> get_max_created_at
with open('/app/src/services/pickup/sync/orders.py') as f:
    content = f.read()
fixed = content.replace('get_max_date()', 'get_max_created_at()')
with open('/app/src/services/pickup/sync/orders.py', 'w') as f:
    f.write(fixed)
print('Sync service fixed')

# 2. Fix DB controller: remove status param, fix service call
with open('/app/src/api/pickup/db/orders.py') as f:
    content = f.read()

content = content.replace(
    'status: str | None = Parameter(default=None, query="status", description="Фильтр по supplierStatus"),',
    ''
).replace(
    'status=status,',
    ''
)
with open('/app/src/api/pickup/db/orders.py', 'w') as f:
    f.write(content)
print('DB controller fixed')

# 3. Check old fields in repo/service
for path in ['/app/src/services/pickup/db/orders.py', '/app/src/repositories/pickup/orders.py']:
    try:
        with open(path) as f:
            c = f.read()
        for bad in ['warehouse_name', 'last_change_date', 'supplier_status', 'order_uid']:
            if bad in c:
                print(f'{path.split("/")[-1]}: BAD -> {bad}')
    except FileNotFoundError:
        print(f'NOT FOUND: {path}')
