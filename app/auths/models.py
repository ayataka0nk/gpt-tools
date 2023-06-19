from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from ..database import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    token = Column(String(256), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False,
                        server_default=func.current_timestamp())
    expires_at = Column(DateTime, nullable=False)
