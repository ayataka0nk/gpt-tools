"""add_column_to_conversation

Revision ID: 6f01ec760af2
Revises: dae745a018c2
Create Date: 2023-06-19 22:13:01.459485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f01ec760af2'
down_revision = 'dae745a018c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('conversations', sa.Column('title', sa.Text, nullable=False))


def downgrade() -> None:
    op.drop_column('conversations', 'title')
