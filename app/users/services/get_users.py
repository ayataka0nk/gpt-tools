from sqlalchemy.orm import Session, load_only
from ..models import User


def get_users(db: Session):
    return db.query(User).options(load_only(User.id, User.email, User.name)).all()
