from pydantic import BaseModel, Field


class Profile(BaseModel):
    user_id: int = Field(..., example=1)
    email: str = Field(..., example="taro_yamada@example.com")
    name: str = Field(..., example="山田太郎")
