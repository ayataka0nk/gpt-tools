"""create refresh token table

Revision ID: 8aea99745e9b
Revises: 54d773c4e895
Create Date: 2023-06-17 20:41:46.934536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aea99745e9b'
down_revision = '54d773c4e895'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'refresh_tokens',
        sa.Column('refresh_token_id', sa.Integer, primary_key=True),
        sa.Column('token', sa.String(256), nullable=False, unique=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey(
            'users.user_id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False,
                  server_default=sa.func.current_timestamp()),
        sa.Column('expires_at', sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('refresh_tokens')
