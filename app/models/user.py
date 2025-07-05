from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger, String, Integer, Enum as SqlEnum,
    ForeignKey, DateTime
)

from app.config.database import Base
from app.common.enums import UserStatus, Role


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(
        SqlEnum(UserStatus, name="user_status"),
        default=UserStatus.UNVERIFIED,
        nullable=False
    )
    role: Mapped[str] = mapped_column(
        SqlEnum(Role, name="user_role"),
        default=Role.USER,
        nullable=False
    )
    
    verify_codes = relationship("VerifyCode", back_populates="user", cascade="all, delete")
    
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")
    blacklist_refresh_tokens = relationship("BlacklistRefreshToken", back_populates="user", cascade="all, delete")


class VerifyCode(Base):
    __tablename__ = "verify_codes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user = relationship("User", back_populates="verify_codes")