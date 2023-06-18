from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from app.users import User

from ..database import get_db
from .schemas import LoginSuccessResponse, ClearTokenRequest
from ..errors import make_responses, UnauthorizedException, ValidationException
from .services import get_user, authenticate, create_tokens, delete_token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post(
    "/token",
    response_model=LoginSuccessResponse,
    responses=make_responses([UnauthorizedException(), ValidationException()]))
def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user_id = authenticate(
        db, email=credentials.username, password=credentials.password)
    tokens = create_tokens(db, user_id)
    return tokens


@router.post(
    "/refresh_token",
    response_model=LoginSuccessResponse,
    responses=make_responses([UnauthorizedException()]))
def refresh_token(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_user)]):
    tokens = create_tokens(db, user.id)
    return tokens


@router.post(
    "/clear_token",
)
def clear_token(request: ClearTokenRequest, db: Annotated[Session, Depends(get_db)]):
    delete_token(db, request.refresh_token)
