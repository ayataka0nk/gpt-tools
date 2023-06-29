from pydantic import BaseModel, Field
from datetime import datetime
from .models import ConversationModel, ConversationMessageModel
from .constants import RoleType
from app.llms import PromptMessage
from . import models


class Conversation(BaseModel):
    conversation_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    title: str = Field(None, example="英会話の練習")
    created_at: datetime = Field(..., example="2020-01-01 00:00:00")

    def from_conversation_model(model: ConversationModel):
        return Conversation(
            conversation_id=model.conversation_id,
            user_id=model.user_id,
            title=model.title,
            created_at=model.created_at,
        )


class ConversationCreate(BaseModel):
    title: str = Field(None, example="英会話の練習")


class ConversationCreateResponse(BaseModel):
    conversation_id: int = Field(..., example=1)


class ConversationUpdate(BaseModel):
    title: str = Field(None, example="英会話の練習")


class ConversationMessage(BaseModel):
    conversation_message_id: int = Field(..., example=1)
    conversation_id: int = Field(..., example=1)
    role_type: int = Field(..., example=1)
    content: str = Field(..., example="こんにちは")
    created_at: datetime = Field(..., example="2020-01-01 00:00:00")

    def from_conversation_message_model(model: ConversationMessageModel):
        return ConversationMessage(
            conversation_message_id=model.conversation_message_id,
            conversation_id=model.conversation_id,
            role_type=model.role_type,
            content=model.content,
            created_at=model.created_at,
        )

    def to_prompt_message(self):
        return PromptMessage(
            role=RoleType(self.role_type).role,
            content=self.content
        )


class ConversationSystemMessage(BaseModel):
    conversation_message_id: int = Field(..., example=1)
    conversation_id: int = Field(..., example=1)
    content: str = Field(..., example="こんにちは")
    created_at: datetime = Field(..., example="2020-01-01 00:00:00")

    def from_conversation_system_message_model(model: models.ConversationSystemMessage):
        return ConversationSystemMessage(
            conversation_message_id=model.conversation_system_message_id,
            conversation_id=model.conversation_id,
            content=model.content,
            created_at=model.created_at,
        )

    def to_prompt_message(self):
        return PromptMessage(
            role='system',
            content=self.content
        )


class PostConversationMessageRequestBody(BaseModel):
    user_message: str = Field(..., example="こんにちは")


class PostConversationSystemMessageRequestBody(BaseModel):
    system_message: str = Field(...,
                                example='あなたは優秀なソフトウェアエンジニアとして、userの相談を受けてください。\nuserはプログラミングについての知識がないので、できるだけわかりやすく説明してください。')
