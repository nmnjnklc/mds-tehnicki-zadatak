from typing import Optional

from src.services.racks import RacksService
from src.services.devices import DevicesService

from src.models.domain.rack import RackDetails, PotentialRack
from src.models.domain.device import Device


class RackEnergyBalancer:
    def __init__(
        self,
        racks_service: RacksService = RacksService(),
        devices_service: DevicesService = DevicesService()
    ):
        self.racks_service = racks_service
        self.devices_service = devices_service

    def balance(self):

        racks: list[RackDetails] = self.racks_service.get_rack_details()
        devices: list[Device] = sorted(self.devices_service.list(), key=lambda d: d.energy_consumption, reverse=True)

        for device in devices:

            potential_rack: Optional[PotentialRack] = None
            least_effective_energy_consumption: float = 1.0

            for i in range(len(racks)):

                if racks[i].available_energy < device.energy_consumption:
                    continue

                if racks[i].available_units < device.units_required:
                    continue

                new_effective_energy_consumption = (
                       racks[i].current_energy_consumption + device.energy_consumption
                ) / racks[i].energy_consumption_capacity

                if new_effective_energy_consumption < least_effective_energy_consumption:
                    least_effective_energy_consumption = new_effective_energy_consumption
                    potential_rack = PotentialRack(index=i, rack=racks[i])

            if potential_rack is not None:
                self.devices_service.update(entity_id=device.id, rack_id=potential_rack.rack.id)
                racks[potential_rack.index] = self.racks_service.get_rack_details(rack_id=potential_rack.rack.id)[0]
