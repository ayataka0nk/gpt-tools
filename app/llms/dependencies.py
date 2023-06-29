from typing import Annotated
from config import Settings, get_settings
from fastapi import Depends
from .chat_completion import ChatCompletion, ChatCompletionGpt3p5Turbo
from . import chat_completion


def create_chat_completion_gpt3p5turbo(settings: Annotated[Settings, Depends(get_settings)]) -> ChatCompletion:
    return ChatCompletionGpt3p5Turbo(api_key=settings.openai_api_key)


def chat_completion_service_factory(settings: Annotated[Settings, Depends(get_settings)]) -> ChatCompletion:
    return chat_completion.ChatCompletionServiceFactory(settings=settings)
