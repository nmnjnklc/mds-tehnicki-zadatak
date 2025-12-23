from pydantic import BaseModel, Field, model_validator
from typing import Optional

from src.models.domain.device import Device


class Rack(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(default=None)
    serial_number: str
    unit_capacity: int
    energy_consumption_capacity: int

    class Config:
        populate_by_name = True
        from_attributes = True


class RackCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    serial_number: str
    unit_capacity: int
    energy_consumption_capacity: int


class RackUpdate(RackCreate): pass


class RackDetails(Rack):
    units_taken: int = Field(default=0)
    available_units: int = Field(default=0)
    available_energy: int = Field(default=0)
    current_energy_consumption: int = Field(default=0)
    current_energy_consumption_percentage: int = Field(default=0)
    effective_energy_consumption: float = Field(default=0.0)
    devices: list[Device]

    @model_validator(mode="after")
    def validate_rack_data(self):

        self.units_taken = 0
        self.available_units = 0
        self.available_energy = 0
        self.current_energy_consumption = 0
        self.current_energy_consumption_percentage = 0
        self.effective_energy_consumption = 0

        for device in self.devices:
            self.current_energy_consumption += device.energy_consumption
            self.units_taken += device.units_required

        self.current_energy_consumption_percentage = round(
            (self.current_energy_consumption / self.energy_consumption_capacity) * 100
        )

        self.effective_energy_consumption = self.current_energy_consumption / self.energy_consumption_capacity

        self.available_units = self.unit_capacity - self.units_taken

        self.available_energy = self.energy_consumption_capacity - self.current_energy_consumption

        return self


class PotentialRack(BaseModel):
    index: int
    rack: RackDetails
