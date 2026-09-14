from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class MemberDB(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class ExpenseDB(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Float)
    paid_by: Mapped[int] = mapped_column(ForeignKey("members.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    participants: Mapped[list["ExpenseParticipant"]] = relationship(
        back_populates="expense", cascade="all, delete-orphan"
    )


class ExpenseParticipant(Base):
    """Join row: which members split a given expense (many-to-many)."""

    __tablename__ = "expense_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))

    expense: Mapped["ExpenseDB"] = relationship(back_populates="participants")
