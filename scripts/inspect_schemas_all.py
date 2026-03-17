"""Inspect key schema fields for DB model creation."""
import importlib.util, sys, inspect
sys.path.insert(0, 'C:/Python/wb-collector/src')

modules_to_check = [
    ('schemas.products.cards', ['ProductCard']),
    ('schemas.products.prices', ['PriceItem']),
    ('schemas.fbs.orders', ['FBSOrder']),
    ('schemas.dbw.orders', ['DBWOrder']),
    ('schemas.dbs.orders', ['DBSOrder']),
    ('schemas.reports.main_reports', ['StockItem', 'OrderReportItem', 'SaleReportItem']),
    ('schemas.finances.finances', ['FinancialReportItem']),
]

for mod_path, classes in modules_to_check:
    try:
        mod = __import__(mod_path, fromlist=classes)
        for cls_name in classes:
            cls = getattr(mod, cls_name, None)
            if cls is None:
                continue
            print(f'\n=== {cls_name} ===')
            for name, field in cls.model_fields.items():
                ann = str(field.annotation)
                print(f'  {name}: {ann}')
    except Exception as e:
        print(f'ERROR {mod_path}: {e}')
