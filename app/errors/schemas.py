from typing import Dict, List
from pydantic import BaseModel


class UnauthorizedErrorContent(BaseModel):
    messages: List[str]


class ValidationErrorContent(BaseModel):
    errors: Dict[str, List[str]]
