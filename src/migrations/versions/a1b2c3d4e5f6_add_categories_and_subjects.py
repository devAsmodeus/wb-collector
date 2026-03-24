"""add_categories_and_subjects

Revision ID: a1b2c3d4e5f6
Revises: 9aba171a7828
Create Date: 2026-03-24 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '9aba171a7828'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- wb_categories ---
    op.create_table('wb_categories',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False, comment='ID категории WB'),
        sa.Column('name', sa.String(length=255), nullable=False, comment='Название категории'),
        sa.Column('parent_id', sa.Integer(), nullable=True, comment='ID родительской категории'),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=False, comment='Дата синхронизации'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_wb_categories_category_id'), 'wb_categories', ['category_id'], unique=True)

    # --- wb_subjects ---
    op.create_table('wb_subjects',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=False, comment='ID предмета WB'),
        sa.Column('name', sa.String(length=255), nullable=False, comment='Название предмета'),
        sa.Column('parent_id', sa.Integer(), nullable=True, comment='ID родительской категории (FK → wb_categories.category_id)'),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=False, comment='Дата синхронизации'),
        sa.ForeignKeyConstraint(['parent_id'], ['wb_categories.category_id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_wb_subjects_subject_id'), 'wb_subjects', ['subject_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_wb_subjects_subject_id'), table_name='wb_subjects')
    op.drop_table('wb_subjects')
    op.drop_index(op.f('ix_wb_categories_category_id'), table_name='wb_categories')
    op.drop_table('wb_categories')
