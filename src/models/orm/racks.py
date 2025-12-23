from sqlalchemy import Column, UniqueConstraint, Integer, String
from sqlalchemy.orm import relationship

from src.models.orm.base import Base


class Racks(Base):
    __tablename__ = "racks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
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

    unit_capacity = Column(
        Integer,
        nullable=False,
    )

    energy_consumption_capacity = Column(
        Integer,
        nullable=False
    )

    devices = relationship("Devices", back_populates="rack")

    __table_args__ = (
        UniqueConstraint(serial_number, name="uq_rack_serial_number"),
    )
