from enum import Enum


class LLMModelType(Enum):
    GPT_3p5 = (1, 'gpt-3.5-turbo')
    GPT_4 = (2, 'gpt-4')

    def __init__(self, id: int, model: str) -> None:
        super().__init__()
        self.id = id
        self.model = model

    @classmethod
    def value_of(cls, id: int):
        for e in LLMModelType:
            print(type(id))
            if e.id == id:
                return e
        raise ValueError('invalid id')
