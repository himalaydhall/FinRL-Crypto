"""
Trade ORM Model
Compatible with both PostgreSQL and SQLite.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    portfolio_id: Mapped[str] = mapped_column(String(36), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    side: Mapped[str] = mapped_column(String(4), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    exit_price: Mapped[float | None] = mapped_column(Float)
    realized_pnl: Mapped[float | None] = mapped_column(Float)
    pnl_percentage: Mapped[float | None] = mapped_column(Float)
    fees: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(12), default="FILLED")
    signal_source: Mapped[str | None] = mapped_column(String(50))
    confidence: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="trades")


class TradeHistory(Base):
    __tablename__ = "trade_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    trade_id: Mapped[str] = mapped_column(String(36), ForeignKey("trades.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    trade = relationship("Trade", back_populates="history")
