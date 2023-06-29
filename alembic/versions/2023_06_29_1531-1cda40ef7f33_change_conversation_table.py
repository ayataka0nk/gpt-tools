"""change conversation table

Revision ID: 1cda40ef7f33
Revises: cd1a7607c830
Create Date: 2023-06-29 15:31:09.908264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cda40ef7f33'
down_revision = 'cd1a7607c830'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('conversations', sa.Column(
        'model_type', sa.Integer, nullable=False))


def downgrade() -> None:
    op.drop_column('conversations', 'model_type')
