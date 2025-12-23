from src.repositories.base import AbstractBaseRepository, BaseRepository
from src.models.orm.devices import Devices


class DevicesAbstractRepository(AbstractBaseRepository):
    pass


class DevicesRepository(BaseRepository[Devices]):
    db_model = Devices
