from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends
from . import services
from ..database import get_db

router = APIRouter(
    prefix='/users'
)


@router.get("/")
def get_users_api(db: Annotated[Session, Depends(get_db)]):
    users = services.get_users(db)
    return users
