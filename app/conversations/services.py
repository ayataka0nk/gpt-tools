import openai
from typing import List
from sqlalchemy import select
from app.database import Session
from .models import ConversationModel
from .schemas import Conversation, ConversationCreate, ConversationUpdate


def get_conversations(user_id: int, db: Session) -> List[Conversation]:
    statement = select(ConversationModel).where(
        ConversationModel.user_id == user_id).order_by(ConversationModel.created_at.desc())
    conversations = db.execute(statement).scalars().all()
    return list(map(lambda conversation: Conversation.fromConversationModel(conversation), conversations))


def create_conversation(user_id: int, conversation: ConversationCreate, db: Session):
    conversation_model = ConversationModel(
        user_id=user_id,
        title=conversation.title)
    db.add(conversation_model)
    db.commit()
    db.refresh(conversation_model)
    return conversation_model


def update_conversation(conversation_id: int, conversation: ConversationUpdate, db: Session):
    statement = select(ConversationModel).where(
        ConversationModel.conversation_id == conversation_id)
    conversation_model = db.execute(statement).scalar_one()
    conversation_model.title = conversation.title
    db.add(conversation_model)
    db.commit()


def create_chat_completion(api_key: str):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": " AIアシスタントの名前はモラグ・バルです。"},
        {"role": "user", "content": " こんにちは。私はあやたかです。あなたは誰ですか？"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, stream=True)
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        word = delta.get('content')
        if (word is None):
            continue
        yield word
