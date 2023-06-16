"""create user table

Revision ID: 54d773c4e895
Revises: 
Create Date: 2023-06-16 16:01:57.874397

""" 
from alembic import op 
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d773c4e895'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.UniqueConstraint('email'),
    )


def downgrade() -> None:
    op.drop_table('users')
