"""create system message table

Revision ID: 97c7921a3a74
Revises: 6f01ec760af2
Create Date: 2023-06-26 19:42:25.199259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c7921a3a74'
down_revision = '6f01ec760af2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'conversation_system_messages',
        sa.Column('conversation_system_message_id',
                  sa.Integer, primary_key=True),
        sa.Column('conversation_id', sa.Integer, sa.ForeignKey(
            'conversations.conversation_id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False,
                  server_default=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table('conversation_system_messages')
