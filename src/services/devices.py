from src.repositories.uow import AbstractUnitOfWork, UnitOfWork
from src.services.base import BaseService

from src.models.domain.device import Device


class DevicesService(BaseService[Device]):
    def __init__(
        self, uow: AbstractUnitOfWork = UnitOfWork(),
    ):
        super().__init__(uow, Device, "devices")
