from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from .services import create_chat_completion
from config import Settings, get_settings
from app.users import User
from app.auths import get_user
from .models import ConversationModel
from .schemas import Conversation

router = APIRouter(
    prefix='/conversations',
    tags=['conversations']
)


@router.get('/', response_model=List[Conversation])
def get_conversations(user: Annotated[User, Depends(get_user)]):
    conversations: List[ConversationModel] = user.conversations
    return list(map(lambda conversation: ConversationModel.toConversation(conversation), conversations))


@router.post('/request-reply')
def request_reply(user: Annotated[User, Depends(get_user)], settings: Annotated[Settings, Depends(get_settings)]):
    result = create_chat_completion(api_key=settings.openai_api_key)
    return StreamingResponse(result, media_type="text/event-stream")
