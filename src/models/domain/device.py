from pydantic import BaseModel, Field
from typing import Optional


class Device(BaseModel):
    id: int
    rack_id: Optional[int] = Field(default=None)
    name: str
    description: Optional[str] = Field(default=None)
    serial_number: str
    units_required: int
    energy_consumption: int

    class Config:
        populate_by_name = True
        from_attributes = True


class DeviceCreate(BaseModel):
    rack_id: Optional[int] = Field(default=None)
    name: str
    description: Optional[str] = Field(default=None)
    serial_number: str
    units_required: int
    energy_consumption: int


class DeviceUpdate(DeviceCreate): pass


class DeviceAssignment(BaseModel):
    device_id: int
    rack_id: int
