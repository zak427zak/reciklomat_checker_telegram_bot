from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class ReciklomatSubscription(Base, TimestampMixin, TableNameMixin):
    """
    Represents a subscription to a reciklomat by a user.

    Attributes:
        id (Mapped[int]): Unique identifier for the subscription.
        user_id (Mapped[int]): ID of the subscribing user.
        reciklomat_address (Mapped[str]): Address of the subscribed reciklomat.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    reciklomat_address: Mapped[str] = mapped_column(String(500))

    def __repr__(self):
        return f"<ReciklomatSubscription {self.reciklomat_address}>"
