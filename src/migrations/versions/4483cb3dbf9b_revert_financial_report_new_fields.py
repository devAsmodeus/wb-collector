"""revert financial_report new fields

Revision ID: 4483cb3dbf9b
Revises: 292776980fc3
Create Date: 2026-04-10 10:41:38.842599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4483cb3dbf9b'
down_revision: Union[str, None] = '292776980fc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('financial_report', 'article_substitution')
    op.drop_column('financial_report', 'sale_price_affiliated_discount_prc')
    op.drop_column('financial_report', 'sale_price_wholesale_discount_prc')


def downgrade() -> None:
    op.add_column('financial_report', sa.Column('sale_price_wholesale_discount_prc', sa.Numeric(8, 2), nullable=True))
    op.add_column('financial_report', sa.Column('sale_price_affiliated_discount_prc', sa.Numeric(8, 2), nullable=True))
    op.add_column('financial_report', sa.Column('article_substitution', sa.BigInteger(), nullable=True))
