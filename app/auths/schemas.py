from pydantic import BaseModel, Field


class Credentials(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="dummy")


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class LoginSuccessResponse(Tokens):
    pass


class ClearTokenRequest(BaseModel):
    refresh_token: str = Field(..., example="foorbar")
