from sqlalchemy import Column, ForeignKey, UniqueConstraint, Integer, String
from sqlalchemy.orm import relationship

from src.models.orm.base import Base


class Devices(Base):
    __tablename__ = "devices"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    rack_id = Column(
        Integer,
        ForeignKey("racks.id"),
        nullable=True
    )

    name = Column(
        String(length=255),
        nullable=False
    )

    description = Column(
        String(length=255),
        nullable=True
    )

    serial_number = Column(
        String(length=255),
        nullable=False
    )

    units_required = Column(
        Integer,
        nullable=False,
    )

    energy_consumption = Column(
        Integer,
        nullable=False
    )

    rack = relationship("Racks", back_populates="devices")

    __table_args__ = (
        UniqueConstraint(serial_number, name="uq_device_serial_number"),
    )