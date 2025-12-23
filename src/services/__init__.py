from src.services.racks import RacksService
from src.services.devices import DevicesService
from src.services.rack_energy_balancer import RackEnergyBalancer

racks_service: RacksService = RacksService()
devices_service: DevicesService = DevicesService()
balancer: RackEnergyBalancer = RackEnergyBalancer()
