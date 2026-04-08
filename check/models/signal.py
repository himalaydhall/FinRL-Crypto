"""
AISignal, Watchlist, PriceAlert, ExchangeCredential, RefreshToken ORM Models
Compatible with both PostgreSQL and SQLite.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Float, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


class AISignal(Base):
    __tablename__ = "ai_signals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    action: Mapped[str] = mapped_column(String(4), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    position_size: Mapped[float | None] = mapped_column(Float)
    expected_return: Mapped[float | None] = mapped_column(Float)
    risk_score: Mapped[float | None] = mapped_column(Float)
    model_id: Mapped[str | None] = mapped_column(String(100))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Watchlist(Base):
    __tablename__ = "watchlists"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbols: Mapped[str] = mapped_column(Text, default="[]")  # JSON-encoded list
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    condition: Mapped[str] = mapped_column(String(10), nullable=False)
    target_value: Mapped[float | None] = mapped_column(Float)
    is_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ExchangeCredential(Base):
    __tablename__ = "exchange_credentials"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exchange: Mapped[str] = mapped_column(String(30), nullable=False, default="binance")
    api_key_enc: Mapped[str] = mapped_column(Text, nullable=False)
    api_secret_enc: Mapped[str] = mapped_column(Text, nullable=False)
    is_testnet: Mapped[bool] = mapped_column(Boolean, default=True)
    permissions: Mapped[str] = mapped_column(Text, default="read,trade")  # Comma-separated
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    device_info: Mapped[str | None] = mapped_column(Text)
    ip_address: Mapped[str | None] = mapped_column(String(45))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
