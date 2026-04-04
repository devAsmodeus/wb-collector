"""rename communications tables: wb_feedbacks -> feedbacks, wb_questions -> questions, wb_claims -> claims

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-04-04 17:30:00.000000

"""
from alembic import op

revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('wb_feedbacks', 'feedbacks')
    op.rename_table('wb_questions', 'questions')
    op.rename_table('wb_claims', 'claims')


def downgrade() -> None:
    op.rename_table('feedbacks', 'wb_feedbacks')
    op.rename_table('questions', 'wb_questions')
    op.rename_table('claims', 'wb_claims')
