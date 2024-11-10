from datetime import datetime
from typing import Optional

from sqlalchemy import Numeric, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class Reciklomat(Base, TimestampMixin, TableNameMixin):
    """
    Represents a recycling machine (Reciklomat) in the system.

    Attributes:
        id (Mapped[int]): Unique identifier for the reciklomat.
        status (Mapped[str]): The current status of the reciklomat.
        occupancy (Mapped[float]): Current occupancy of the reciklomat.
        capacity (Mapped[float]): Total capacity of the reciklomat.
        address (Mapped[str]): Address of the reciklomat.
        city (Mapped[str]): City where the reciklomat is located.
        district (Mapped[str]): District where the reciklomat is located.
        lat (Mapped[float]): Latitude of the reciklomat location.
        lon (Mapped[float]): Longitude of the reciklomat location.
        last_check (Mapped[datetime]): Last time the reciklomat was checked.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(100))
    occupancy: Mapped[float] = mapped_column(Numeric(4, 0))
    capacity: Mapped[float] = mapped_column(Numeric(4, 0))
    address: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(100))
    district: Mapped[str] = mapped_column(String(100))
    lat: Mapped[float] = mapped_column(Numeric(11, 8))
    lon: Mapped[float] = mapped_column(Numeric(11, 8))
    last_check: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __repr__(self):
        return f"<Reciklomat {self.address}>"
