from abc import abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.repositories.base import AbstractBaseRepository, BaseRepository
from src.models.orm.racks import Racks


class RacksAbstractRepository(AbstractBaseRepository):
    @abstractmethod
    def get_rack_details(self, rack_id: Optional[int] = None):
        raise NotImplementedError


class RacksRepository(BaseRepository[Racks]):
    db_model = Racks

    def get_rack_details(self, rack_id: Optional[int] = None):
        statement = select(Racks).options(joinedload(Racks.devices))
        if rack_id:
            statement = statement.filter_by(id=rack_id)
        return self.session.scalars(statement=statement).unique()
