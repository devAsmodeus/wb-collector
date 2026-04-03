"""rename_tables_and_fix_seller_tin

Revision ID: defac75f119b
Revises: cca7df82e106
Create Date: 2026-04-03 13:49:02.891506

Изменения:
- wb_news → news
- wb_seller_rating → seller_rating
- wb_seller_subscriptions → seller_subscriptions
- sellers.itn → sellers.tin (поле WB API называется tin, не itn)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'defac75f119b'
down_revision: Union[str, None] = 'cca7df82e106'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Переименование таблиц
    op.rename_table('wb_news', 'news')
    op.rename_table('wb_seller_rating', 'seller_rating')
    op.rename_table('wb_seller_subscriptions', 'seller_subscriptions')

    # Переименование колонки itn → tin в sellers
    op.alter_column('sellers', 'itn', new_column_name='tin')


def downgrade() -> None:
    op.alter_column('sellers', 'tin', new_column_name='itn')
    op.rename_table('seller_subscriptions', 'wb_seller_subscriptions')
    op.rename_table('seller_rating', 'wb_seller_rating')
    op.rename_table('news', 'wb_news')
