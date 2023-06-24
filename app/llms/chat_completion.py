from abc import ABCMeta, abstractmethod
from typing import Generator
from .schemas import PromptMessage
import openai


class ChatCompletion(metaclass=ABCMeta):

    @abstractmethod
    def stream(self, promptMessages: PromptMessage) -> Generator[str, None, None]:
        raise NotImplementedError()

    @abstractmethod
    def create(self, promptMessages: PromptMessage) -> str:
        raise NotImplementedError()


class ChatCompletionGpt3p5Turbo(ChatCompletion):

    def __init__(self, api_key: str) -> None:
        super().__init__()
        openai.api_key = api_key

    def stream(self, promptMessages):
        messages = list(map(lambda message: message.dict(), promptMessages))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, stream=True)
        for chunk in response:
            delta = chunk['choices'][0]['delta']
            word = delta.get('content')
            if (word is None):
                continue
            yield word

    def create(self, promptMessages):
        raise NotImplementedError()
