from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from .services import create_chat_completion
from config import Settings, get_settings

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


@router.post('/request-reply')
def request_reply(settings: Annotated[Settings, Depends(get_settings)]):
    result = create_chat_completion(api_key=settings.openai_api_key)
    return StreamingResponse(result, media_type="text/event-stream")
