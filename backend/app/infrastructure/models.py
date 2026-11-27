from datetime import datetime, time

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    access_rule: Mapped["AccessRuleModel | None"] = relationship(back_populates="user", uselist=False)


class AccessRuleModel(Base):
    __tablename__ = "access_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    weekdays: Mapped[list[int]] = mapped_column(JSON, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    access_points: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    user: Mapped[UserModel] = relationship(back_populates="access_rule")


class AccessAttemptModel(Base):
    __tablename__ = "access_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    access_point: Mapped[str] = mapped_column(String(80), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    decision: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
