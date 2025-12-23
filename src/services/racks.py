from typing import Optional

from src.repositories.uow import AbstractUnitOfWork, UnitOfWork
from src.services.base import BaseService

from src.models.domain.rack import Rack, RackDetails


class RacksService(BaseService[Rack]):
    def __init__(
        self,
        uow: AbstractUnitOfWork = UnitOfWork(),
    ):
        super().__init__(uow, Rack, "racks")

    def get_rack_details(self, rack_id: Optional[int] = None):
        with self.uow:
            rack_details = [
                RackDetails.model_validate(obj=rack) for rack in self.uow.racks.get_rack_details(rack_id=rack_id)
            ]
        return rack_details
