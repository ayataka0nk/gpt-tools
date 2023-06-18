from fastapi import APIRouter
from fastapi import Depends
from app.auths import get_user
from app.users import User
from app.errors import make_responses, UnauthorizedException
from .schemas import Profile


router = APIRouter(
    prefix='/profile'
)


@router.get('', response_model=Profile, responses=make_responses([
    UnauthorizedException()]))
def get_profile(user: User = Depends(get_user)):
    return Profile(
        id=user.id,
        email=user.email,
        name=user.name
    )
