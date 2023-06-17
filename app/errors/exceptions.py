from .schemas import ValidationErrorContent
from typing import Union
from fastapi import status, HTTPException


class MyHTTPException(HTTPException):
    description = 'API error'
    model = None


class UnauthorizedException(MyHTTPException):
    description = "認証失敗"

    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)


class ValidationException(MyHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    description = "バリデーションエラー。入力のkeyを使ったdictでエラー内容を返す。配列はfoo.0やfoo.0.barのように表す。"
    model = ValidationErrorContent
    content: Union[ValidationErrorContent, None]

    def __init__(self, content=None):
        self.content = content
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
