"""rename promotion tables: wb_campaigns -> campaigns, wb_campaign_stats -> campaign_stats, wb_promotions -> promotions

Revision ID: c3d4e5f6a7b8
Revises: a650ee1b4fc8
Create Date: 2026-04-04 17:00:00.000000

"""
from alembic import op

revision = 'c3d4e5f6a7b8'
down_revision = 'a650ee1b4fc8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('wb_campaigns', 'campaigns')
    op.rename_table('wb_campaign_stats', 'campaign_stats')
    op.rename_table('wb_promotions', 'promotions')


def downgrade() -> None:
    op.rename_table('campaigns', 'wb_campaigns')
    op.rename_table('campaign_stats', 'wb_campaign_stats')
    op.rename_table('promotions', 'wb_promotions')
