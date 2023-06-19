"""create_conversation_table

Revision ID: dae745a018c2
Revises: 8aea99745e9b
Create Date: 2023-06-19 20:59:06.124854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae745a018c2'
down_revision = '8aea99745e9b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'conversations',
        sa.Column('conversation_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey(
            'users.user_id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False,
                  server_default=sa.func.current_timestamp()),
    )
    op.create_table(
        'conversation_messages',
        sa.Column('conversation_message_id', sa.Integer, primary_key=True),
        sa.Column('conversation_id', sa.Integer, sa.ForeignKey(
            'conversations.conversation_id'), nullable=False),
        sa.Column('role_type', sa.Integer, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False,
                  server_default=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table('conversation_messages')
    op.drop_table('conversations')
