from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends
from . import services
from ..database import get_db
from .schemas import Credentials, LoginSuccessResponse
from ..errors import make_responses, UnauthorizedException, ValidationException

router = APIRouter(
    prefix='/auth'
)


@router.post(
    "/login",
    response_model=LoginSuccessResponse,
    responses=make_responses([UnauthorizedException(), ValidationException()]))
def login(credentials: Credentials, db: Annotated[Session, Depends(get_db)]):
    user_id = services.authenticate(
        db, credentials.email, credentials.password)
    tokens = services.create_tokens(db, user_id)
    return tokens
