import sqlalchemy as sa
from ..database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    user_id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(length=255), nullable=False)
    password = sa.Column(sa.String(length=255), nullable=False)
    name = sa.Column(sa.String(length=255), nullable=False)

    conversations = relationship("ConversationModel", back_populates="user")

    def verify_password(self, password):
        return self.password == password
