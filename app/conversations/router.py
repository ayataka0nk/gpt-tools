from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.users import User
from app.auths import get_user

from .schemas import (
    Conversation,
    ConversationCreate,
    ConversationCreateResponse,
    ConversationUpdate,
    ConversationMessage,
    PostConversationMessageRequestBody,
    PostConversationSystemMessageRequestBody
)
from ..database import get_db, Session

from app import llms
from . import services, schemas

from .services import (
    get_conversations,
    create_conversation,
    update_conversation,
    get_conversation_messages,
    post_conversation_message,
    create_or_update_conversation_settings,
    get_conversation
)
from .dependencies import valid_user_conversation_id


router = APIRouter(
    prefix='/conversations',
    tags=['conversations']
)


@router.get('', response_model=list[Conversation])
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


@router.get('/{conversation_id}', response_model=Conversation)
def get_conversation_api(conversation_id: Annotated[int, Depends(valid_user_conversation_id)], db: Annotated[Session, Depends(get_db)]):
    return get_conversation(conversation_id=conversation_id, db=db)


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


@router.get('/{conversation_id}/messages', response_model=list[ConversationMessage])
def get_conversation_messages_api(
        conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
        db: Annotated[Session, Depends(get_db)]):
    return get_conversation_messages(conversation_id=conversation_id, db=db)


@router.post('/{conversation_id}/messages')
def post_conversation_message_api(
    conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
    body: PostConversationMessageRequestBody,
    db: Annotated[Session, Depends(get_db)],
    chat_completion_service_factory: Annotated[llms.ChatCompletion, Depends(llms.chat_completion_service_factory)],
):
    result = post_conversation_message(
        conversation_id=conversation_id,
        user_message_content=body.user_message,
        db=db,
        chat_completion_service_factory=chat_completion_service_factory)
    return StreamingResponse(result, media_type="text/event-stream")


@router.get('/{conversation_id}/system-messages', response_model=schemas.ConversationSystemMessage)
def get_system_message_api(
    conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
    db: Annotated[Session, Depends(get_db)],
):
    system_message = services.get_system_message(
        conversation_id=conversation_id, db=db)
    if (system_message is None):
        # 404を返す
        raise HTTPException(status_code=404, detail="System Message Not Found")
    else:
        return system_message


@ router.put('/{conversation_id}/system-messages')
def post_system_message_api(
    conversation_id: Annotated[int, Depends(valid_user_conversation_id)],
    body: PostConversationSystemMessageRequestBody,
    db: Annotated[Session, Depends(get_db)],
):
    conversation_system_message_id = create_or_update_conversation_settings(
        conversation_id=conversation_id,
        modelType=llms.LLMModelType.value_of(body.model_type),
        system_message_content=body.system_message,
        db=db)
    return {
        conversation_system_message_id: conversation_system_message_id
    }
