from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from config import Settings, get_settings
from app.users import User
from app.auths import get_user

from .schemas import Conversation, ConversationCreate, ConversationCreateResponse, ConversationUpdate
from ..database import get_db, Session
from .services import create_chat_completion, get_conversations, create_conversation, update_conversation

from .dependencies import valid_user_conversation_id


router = APIRouter(
    prefix='/conversations',
    tags=['conversations']
)


@router.get('', response_model=List[Conversation])
def get_conversations_api(user: Annotated[User, Depends(get_user)], db: Annotated[Session, Depends(get_db)]):
    return get_conversations(db=db, user_id=user.user_id)


@router.post('', response_model=ConversationCreateResponse)
def create_conversation_api(
        user: Annotated[User, Depends(get_user)],
        body: ConversationCreate,
        db: Annotated[Session, Depends(get_db)]):
    conversation_model = create_conversation(
        user_id=user.user_id, conversation=body, db=db)
    return ConversationCreateResponse(conversation_id=conversation_model.conversation_id)


@router.patch('/{conversation_id}', status_code=204)
def update_conversation_api(
        conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
        body: ConversationUpdate,
        db: Annotated[Session, Depends(get_db)]):
    update_conversation(
        conversation_id=conversation_id,
        conversation=body,
        db=db
    )
    return


@router.post('/request-reply')
def request_reply(user: Annotated[User, Depends(get_user)], settings: Annotated[Settings, Depends(get_settings)]):
    result = create_chat_completion(api_key=settings.openai_api_key)
    return StreamingResponse(result, media_type="text/event-stream")
