from typing import Annotated
from config import Settings, get_settings
from fastapi import Depends
from .chat_completion import ChatCompletion, ChatCompletionGpt3p5Turbo


def create_chat_completion_gpt3p5turbo(settings: Annotated[Settings, Depends(get_settings)]) -> ChatCompletion:
    return ChatCompletionGpt3p5Turbo(api_key=settings.openai_api_key)
