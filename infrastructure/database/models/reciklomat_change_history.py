from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class ReciklomatChangeHistory(Base, TimestampMixin, TableNameMixin):
    """
    Represents the history of changes in the reciklomat's status.

    Attributes:
        id (Mapped[int]): Unique identifier for the change history entry.
        reciklomat_id (Mapped[int]): ID of the reciklomat.
        old_status (Mapped[str]): Previous status of the reciklomat.
        new_status (Mapped[str]): New status of the reciklomat.
        change_date (Mapped[datetime]): Date and time of the status change.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reciklomat_id: Mapped[int] = mapped_column(Integer, index=True)
    old_status: Mapped[str] = mapped_column(String(100))
    new_status: Mapped[str] = mapped_column(String(100))
    change_date: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<ReciklomatChangeHistory {self.reciklomat_id} {self.old_status} -> {self.new_status}>"
