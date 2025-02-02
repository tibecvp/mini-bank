import uuid
from sqlalchemy import Column, String, Boolean, DECIMAL, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())
    sessions = relationship("Session", back_populates="user")

    @classmethod
    def check_password(cls, **kwargs):
        user = kwargs.get("user")
        print("PWD_HASH", user)
        print(kwargs.get("password"))
        password = kwargs.get("password")
        if user.password_hash == password:
            return True
        return False


class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(UUID(as_uuid=True),
                        primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.user_id'), nullable=False)
    # Adjust the length based on your JWT size
    jwt_token = Column(String(500), nullable=False)
    refresh_token = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="sessions")
