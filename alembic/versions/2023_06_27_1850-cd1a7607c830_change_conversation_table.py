"""change conversation table

Revision ID: cd1a7607c830
Revises: 97c7921a3a74
Create Date: 2023-06-27 18:50:46.692622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd1a7607c830'
down_revision = '97c7921a3a74'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('conversations', 'title',
                    existing_type=sa.Text,
                    existing_nullable=False,
                    nullable=True)


def downgrade() -> None:
    op.alter_column('conversations', 'title',
                    existing_type=sa.Text,
                    existing_nullable=True,
                    nullable=False)
