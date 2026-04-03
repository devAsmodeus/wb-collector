"""rename_products_tables_fix_fields

Revision ID: 5e6b2d9a5178
Revises: 89e199b021cd
Create Date: 2026-04-03

Изменения:
- wb_cards → cards (+add dimensions_valid)
- wb_prices → prices (rename club_price→club_discount, editable→editable_size_price,
                       drop price+discounted_price, add sizes JSON + is_bad_turnover)
- wb_tags → tags
- wb_seller_warehouses → seller_warehouses (drop old fields, add office_id etc.)
- wb_categories → categories
- wb_subjects → subjects (убран FK)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5e6b2d9a5178'
down_revision: Union[str, None] = '89e199b021cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Простые переименования
    op.rename_table('wb_cards', 'cards')
    op.rename_table('wb_tags', 'tags')
    op.rename_table('wb_categories', 'categories')

    # 2. subjects — убираем FK перед переименованием
    op.execute('ALTER TABLE wb_subjects DROP CONSTRAINT IF EXISTS wb_subjects_parent_id_fkey')
    op.rename_table('wb_subjects', 'subjects')

    # 3. prices — переименовываем колонки, удаляем старые, добавляем новые
    op.rename_table('wb_prices', 'prices')
    op.execute('ALTER TABLE prices RENAME COLUMN club_price TO club_discount')
    op.execute('ALTER TABLE prices RENAME COLUMN editable TO editable_size_price')
    op.execute('ALTER TABLE prices DROP COLUMN IF EXISTS price')
    op.execute('ALTER TABLE prices DROP COLUMN IF EXISTS discounted_price')
    op.execute('ALTER TABLE prices DROP COLUMN IF EXISTS currency_iso_code')
    op.execute('ALTER TABLE prices ADD COLUMN IF NOT EXISTS sizes JSONB')
    op.execute('ALTER TABLE prices ADD COLUMN IF NOT EXISTS currency_iso_code VARCHAR(10)')
    op.execute('ALTER TABLE prices ADD COLUMN IF NOT EXISTS is_bad_turnover BOOLEAN')
    # Меняем тип club_discount и editable_size_price
    op.execute('ALTER TABLE prices ALTER COLUMN club_discount TYPE INTEGER USING club_discount::INTEGER')
    op.execute('ALTER TABLE prices ALTER COLUMN discount TYPE INTEGER USING discount::INTEGER')

    # 4. seller_warehouses — переименовываем + меняем поля
    op.rename_table('wb_seller_warehouses', 'seller_warehouses')
    op.execute('ALTER TABLE seller_warehouses DROP COLUMN IF EXISTS address')
    op.execute('ALTER TABLE seller_warehouses DROP COLUMN IF EXISTS work_time')
    op.execute('ALTER TABLE seller_warehouses DROP COLUMN IF EXISTS selected_coefficient')
    op.execute('ALTER TABLE seller_warehouses ADD COLUMN IF NOT EXISTS office_id BIGINT')
    op.execute('ALTER TABLE seller_warehouses ADD COLUMN IF NOT EXISTS cargo_type INTEGER')
    op.execute('ALTER TABLE seller_warehouses ADD COLUMN IF NOT EXISTS delivery_type INTEGER')
    op.execute('ALTER TABLE seller_warehouses ADD COLUMN IF NOT EXISTS is_deleting BOOLEAN')
    op.execute('ALTER TABLE seller_warehouses ADD COLUMN IF NOT EXISTS is_processing BOOLEAN')

    # 5. cards — добавляем новое поле
    op.execute('ALTER TABLE cards ADD COLUMN IF NOT EXISTS dimensions_valid BOOLEAN')
    op.execute('ALTER TABLE cards ALTER COLUMN length TYPE INTEGER USING length::INTEGER')
    op.execute('ALTER TABLE cards ALTER COLUMN width TYPE INTEGER USING width::INTEGER')
    op.execute('ALTER TABLE cards ALTER COLUMN height TYPE INTEGER USING height::INTEGER')


def downgrade() -> None:
    op.rename_table('cards', 'wb_cards')
    op.rename_table('prices', 'wb_prices')
    op.rename_table('tags', 'wb_tags')
    op.rename_table('seller_warehouses', 'wb_seller_warehouses')
    op.rename_table('categories', 'wb_categories')
    op.rename_table('subjects', 'wb_subjects')
