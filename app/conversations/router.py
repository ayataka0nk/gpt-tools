from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from config import Settings, get_settings
from app.users import User
from app.auths import get_user

from .schemas import (
    Conversation,
    ConversationCreate,
    ConversationCreateResponse,
    ConversationUpdate,
    ConversationMessage,
    PostConversationMessageRequestBody
)
from ..database import get_db, Session

from .services import (
    get_conversations,
    create_conversation,
    update_conversation,
    get_conversation_messages,
    post_conversation_message
)
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


@router.get('/{conversation_id}/messages', response_model=List[ConversationMessage])
def get_conversation_messages_api(
        conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
        db: Annotated[Session, Depends(get_db)]):
    return get_conversation_messages(conversation_id=conversation_id, db=db)


@router.post('/{conversation_id}/messages')
def post_conversation_message_api(
    conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
    body: PostConversationMessageRequestBody,
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)]
):
    result = post_conversation_message(
        conversation_id=conversation_id,
        user_message_content=body.user_message,
        db=db,
        openai_api_key=settings.openai_api_key)
    return StreamingResponse(result, media_type="text/event-stream")
