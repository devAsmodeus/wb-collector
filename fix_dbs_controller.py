with open('/app/src/api/dbs/db/orders.py') as f:
    content = f.read()

content = content.replace(
    'status: str | None = Parameter(default=None, query="status", description="Фильтр по supplierStatus")',
    'delivery_type: str | None = Parameter(default=None, query="delivery_type", description="Фильтр по типу доставки")'
).replace(
    'status=status,',
    'delivery_type=delivery_type,'
)

with open('/app/src/api/dbs/db/orders.py', 'w') as f:
    f.write(content)
print('Fixed')
