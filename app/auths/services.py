from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import load_only
from app.users.models import User
from datetime import datetime, timedelta
from jose import jwt
import os
import base64
from app.database import get_db
from .models import RefreshToken
from .schemas import Tokens
from ..errors.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise UnauthorizedException()
    if not user.verify_password(password):
        raise UnauthorizedException()
    return user.id


def create_access_token(user_id: int):
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'user_id': user_id,
    }
    # TODO: JWTのシークレットキーを環境変数から取得する
    access_token = jwt.encode(
        access_payload, 'SECRET_KEY123', algorithm='HS256')
    return access_token


def create_refresh_token():
    return base64.urlsafe_b64encode(os.urandom(30)).decode()


def create_tokens(db: Session, user_id: str):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token()

    db_refresh_token = RefreshToken(
        user_id=user_id, token=refresh_token, expires_at=datetime.utcnow() + timedelta(days=30))
    db.add(db_refresh_token)
    db.commit()
    return Tokens(access_token=access_token, refresh_token=refresh_token)


def delete_tokens(db: Session, user_id: int):
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()


def delete_token(db: Session, refresh_token: str):
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token).delete()
    db.commit()


def is_jwt(token):
    try:
        header, payload, signature = token.split('.')
    except ValueError:
        # JWTは3つの部分からなるため、splitで3つの部分に分けられない場合はJWTではない
        return False

    if not all([header, payload, signature]):
        # すべての部分が存在する必要がある
        return False

    return True


def get_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    if (is_jwt(token)):
        # TODO: JWTのシークレットキーを環境変数から取得する
        # 有効期限と署名は自動で検証される。
        payload = jwt.decode(token, 'SECRET_KEY123', algorithms=['HS256'])
        # パスワード以外
        user = db.query(User).options(load_only(
            User.id, User.email, User.name
        )) .filter(User.id == payload['user_id']).first()

        if (user is None):
            raise UnauthorizedException()
        return user
    else:
        db_refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == token).first()
        if (db_refresh_token is None):
            raise UnauthorizedException()

        user = db.query(User).options(load_only(
            User.id, User.email, User.name
        )).filter(
            User.id == db_refresh_token.user_id).first()
        if (user is None):
            raise UnauthorizedException()
        return user
