"""fix_orders_schema_v3_api

Revision ID: a650ee1b4fc8
Revises: 5e6b2d9a5178
Create Date: 2026-04-03

Полная переработка схем таблиц заказов.
Убраны поля из Statistics/Reports API (warehouse_name, country_name, spp, discount_percent и др.)
Добавлены правильные поля из WB API v3 Order schema:
  price, converted_price, currency_code, delivery_type, supply_id,
  warehouse_id, office_id, cargo_type, scan_price, address, offices, options
Переименовано: date → created_at
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'a650ee1b4fc8'
down_revision: Union[str, None] = '5e6b2d9a5178'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _fix_orders_table(table: str, has_scan_price: bool = False, has_cross_border: bool = False,
                      has_comment: bool = False, has_options: bool = False,
                      has_color_code: bool = True, has_converted_currency: bool = False) -> None:
    """Унифицированное исправление таблицы заказов."""
    # Убираем старые поля
    for col in ['last_change_date', 'warehouse_name', 'country_name', 'oblast_okrug_name',
                'region_name', 'subject', 'category', 'brand', 'name', 'tech_size',
                'total_price', 'discount_percent', 'spp', 'finished_price', 'price_with_disc',
                'is_cancel', 'cancel_date', 'order_type', 'supplier_status', 'wb_status',
                'delivery_address']:
        op.execute(f'ALTER TABLE {table} DROP COLUMN IF EXISTS {col}')

    # Переименовываем date → created_at
    op.execute(f'ALTER TABLE {table} RENAME COLUMN date TO created_at')

    # Добавляем новые поля
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS price INTEGER')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS converted_price INTEGER')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS currency_code INTEGER')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS converted_currency_code INTEGER')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS delivery_type VARCHAR(20)')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS supply_id VARCHAR(50)')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS warehouse_id BIGINT')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS office_id BIGINT')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS cargo_type INTEGER')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS offices JSONB')
    op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS address JSONB')

    if has_color_code:
        op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS color_code VARCHAR(50)')

    if has_scan_price:
        op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS scan_price INTEGER')

    if has_cross_border:
        op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS cross_border_type INTEGER')

    if has_comment:
        op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS comment VARCHAR(500)')

    if has_options:
        op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS options JSONB')

    if has_converted_currency:
        op.execute(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS converted_currency_code INTEGER')


def upgrade() -> None:
    _fix_orders_table('fbs_orders',
                      has_scan_price=True, has_cross_border=True,
                      has_comment=True, has_options=True, has_converted_currency=True)
    _fix_orders_table('dbw_orders',
                      has_color_code=True)
    _fix_orders_table('dbs_orders',
                      has_color_code=True)
    _fix_orders_table('pickup_orders',
                      has_color_code=False)


def downgrade() -> None:
    # Восстановление не предусмотрено — данные несовместимы
    pass
