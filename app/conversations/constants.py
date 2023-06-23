from enum import Enum


class RoleType(Enum):
    SYSTEM = (1, 'system')
    ASSISTANT = (2, 'assistant')
    USER = (3, 'user')

    def __init__(self, id: int, role: str) -> None:
        super().__init__()
        self.id = id
        self.role = role

    def __new__(cls, id: int, role: str):
        obj = object.__new__(cls)
        cls._value2member_map_[id] = obj
        return obj
