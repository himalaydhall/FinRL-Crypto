"""
User & UserSettings ORM Models
Compatible with both PostgreSQL and SQLite.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, Float, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar_url: Mapped[str | None] = mapped_column(Text)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    trading_mode: Mapped[str] = mapped_column(String(10), default="paper")
    risk_tolerance: Mapped[float] = mapped_column(Float, default=0.5)
    max_position_size: Mapped[float] = mapped_column(Float, default=0.20)
    stop_loss_pct: Mapped[float] = mapped_column(Float, default=0.10)
    active_model_id: Mapped[str] = mapped_column(String(100), default="kcross_trial2")
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    email_alerts: Mapped[bool] = mapped_column(Boolean, default=False)
    theme: Mapped[str] = mapped_column(String(20), default="dark")
    default_timeframe: Mapped[str] = mapped_column(String(10), default="5m")
    auto_execute: Mapped[bool] = mapped_column(Boolean, default=False)
    max_simultaneous_positions: Mapped[int] = mapped_column(Integer, default=10)
    daily_loss_limit: Mapped[float] = mapped_column(Float, default=0.10)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="settings")
