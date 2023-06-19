from pydantic import BaseModel, Field
from datetime import datetime
from .models import ConversationModel


class Conversation(BaseModel):
    conversation_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    title: str = Field(..., example="英会話の練習")
    created_at: datetime = Field(..., example="2020-01-01 00:00:00")

    def fromConversationModel(model: ConversationModel):
        return Conversation(
            conversation_id=model.conversation_id,
            user_id=model.user_id,
            title=model.title,
            created_at=model.created_at,
        )


class ConversationCreate(BaseModel):
    title: str = Field('No Title', example="英会話の練習")


class ConversationCreateResponse(BaseModel):
    conversation_id: int = Field(..., example=1)


class ConversationUpdate(BaseModel):
    title: str = Field(..., example="英会話の練習")


class ConversationMessage(BaseModel):
    conver_message_id: int = Field(..., example=1)
    conversation_id: int = Field(..., example=1)
    role_type: int = Field(..., example=1)
    content: str = Field(..., example="こんにちは")
    created_at: datetime = Field(..., example="2020-01-01 00:00:00")
