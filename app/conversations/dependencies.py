from typing import Annotated
from fastapi import Depends
from app.users import User
from app.auths import get_user
from app.database import Session, get_db
from sqlalchemy import select
from .models import ConversationModel


def valid_user_conversation_id(
        user: Annotated[User, Depends(get_user)],
        conversation_id: int,
        db: Annotated[Session, Depends(get_db)]):
    statement = select(
        ConversationModel
    ).where(
        ConversationModel.user_id == user.user_id
    ).where(
        ConversationModel.conversation_id == conversation_id
    )
    conversation_model = db.execute(statement).scalar_one()
    return conversation_model.conversation_id
