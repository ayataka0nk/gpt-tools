from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from . import services
from ..database import get_db
from .schemas import LoginSuccessResponse
from ..errors import make_responses, UnauthorizedException, ValidationException

router = APIRouter(
    prefix='/auth'
)


@router.post(
    "/token",
    response_model=LoginSuccessResponse,
    responses=make_responses([UnauthorizedException(), ValidationException()]))
def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user_id = services.authenticate(
        db, email=credentials.username, password=credentials.password)
    tokens = services.create_tokens(db, user_id)
    return tokens
