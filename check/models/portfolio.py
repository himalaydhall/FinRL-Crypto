"""
Portfolio, Position, PortfolioSnapshot ORM Models
Compatible with both PostgreSQL and SQLite.
"""

import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    mode: Mapped[str] = mapped_column(String(10), nullable=False, default="paper")
    initial_capital: Mapped[float] = mapped_column(Float, nullable=False, default=100000)
    current_cash: Mapped[float] = mapped_column(Float, nullable=False, default=100000)
    currency: Mapped[str] = mapped_column(String(10), default="USDT")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="portfolio", cascade="all, delete-orphan")
    snapshots = relationship("PortfolioSnapshot", back_populates="portfolio", cascade="all, delete-orphan")


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    portfolio_id: Mapped[str] = mapped_column(String(36), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    side: Mapped[str] = mapped_column(String(5), nullable=False, default="long")
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    avg_entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float | None] = mapped_column(Float)
    unrealized_pnl: Mapped[float | None] = mapped_column(Float)
    allocation_pct: Mapped[float | None] = mapped_column(Float)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    portfolio_id: Mapped[str] = mapped_column(String(36), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    total_value: Mapped[float] = mapped_column(Float, nullable=False)
    cash_balance: Mapped[float] = mapped_column(Float, nullable=False)
    daily_pnl: Mapped[float | None] = mapped_column(Float)
    daily_return: Mapped[float | None] = mapped_column(Float)
    cumulative_return: Mapped[float | None] = mapped_column(Float)
    sharpe_ratio: Mapped[float | None] = mapped_column(Float)
    max_drawdown: Mapped[float | None] = mapped_column(Float)
    win_rate: Mapped[float | None] = mapped_column(Float)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="snapshots")
