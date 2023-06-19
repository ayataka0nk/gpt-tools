import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class ConversationModel(Base):
    __tablename__ = 'conversations'

    conversation_id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(
        'users.user_id'), nullable=False)
    title = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False,
                           server_default=func.current_timestamp())

    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessageModel",
                            back_populates="conversation")


class ConversationMessageModel(Base):
    __tablename__ = 'conversation_messages'

    conversation_message_id = sa.Column(sa.Integer, primary_key=True)
    conversation_id = sa.Column(sa.Integer, sa.ForeignKey(
        'conversations.conversation_id'), nullable=False)
    role_type = sa.Column(sa.Integer, nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False,
                           server_default=func.current_timestamp())

    conversation = relationship("ConversationModel", back_populates="messages")
