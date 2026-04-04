bad_fields = ['warehouse_name', 'last_change_date', 'supplier_status', 'is_cancel', 'get_max_date']
files = [
    '/app/src/repositories/dbs/orders.py',
    '/app/src/services/dbs/db/orders.py',
    '/app/src/services/dbs/sync/orders.py',
]
for path in files:
    with open(path) as f:
        content = f.read()
    name = path.split('/')[-2] + '/' + path.split('/')[-1]
    for bad in bad_fields:
        if bad in content:
            print(f'{name}: BAD -> {bad}')
print('check done')
