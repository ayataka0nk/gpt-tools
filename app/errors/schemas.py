from typing import Dict
from pydantic import BaseModel


class UnauthorizedErrorContent(BaseModel):
    messages: list[str]


class ValidationErrorContent(BaseModel):
    errors: Dict[str, list[str]]
