"""rename reports/finances tables: wb_stocks/orders_report/sales_report/financial_report -> drop wb_ prefix

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-04-04 18:00:00.000000

"""
from alembic import op

revision = 'e5f6a7b8c9d0'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('wb_stocks', 'stocks')
    op.rename_table('wb_orders_report', 'orders_report')
    op.rename_table('wb_sales_report', 'sales_report')
    op.rename_table('wb_financial_report', 'financial_report')


def downgrade() -> None:
    op.rename_table('stocks', 'wb_stocks')
    op.rename_table('orders_report', 'wb_orders_report')
    op.rename_table('sales_report', 'wb_sales_report')
    op.rename_table('financial_report', 'wb_financial_report')
