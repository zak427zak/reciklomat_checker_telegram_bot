# Модель User
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class User(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a user in the Reciklomat application.

    Attributes:
        id (Mapped[int]): The unique identifier of the user.
        telegram_id (Mapped[Optional[str]]): The Telegram ID of the user.
        is_telegram_on (Mapped[bool]): Indicates whether the Telegram is active.
        first_name (Mapped[Optional[str]]): The first name of the user.
        last_name (Mapped[Optional[str]]): The last name of the user.
        username (Mapped[Optional[str]]): The username of the user.
        registred_date (Mapped[Optional[datetime]]): The date when the user registered.
        last_seen (Mapped[Optional[datetime]]): The last time the user was seen.
        language (Mapped[str]): The language preference of the user. Can be 'en', 'ru', or 'sr'.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[Optional[str]] = mapped_column(String(300))
    is_telegram_on: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    first_name: Mapped[Optional[str]] = mapped_column(String(300))
    last_name: Mapped[Optional[str]] = mapped_column(String(300))
    username: Mapped[Optional[str]] = mapped_column(String(300))
    registred_date: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    language: Mapped[str] = mapped_column(Enum("en", "ru", "sr", name="user_language_enum"), nullable=False,
                                          server_default="en")

    def __repr__(self):
        return f"<User {self.id} {self.username}>"
