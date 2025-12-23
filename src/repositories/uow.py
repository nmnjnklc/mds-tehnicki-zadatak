from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src import db_config

from src.repositories.racks import RacksAbstractRepository, RacksRepository
from src.repositories.devices import DevicesAbstractRepository, DevicesRepository


class AbstractUnitOfWork(ABC):
    racks: RacksAbstractRepository
    devices: DevicesAbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    def add_all(self, *args):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        url=db_config.get_db_uri(),
        pool_size=10,
        max_overflow=10,
        pool_recycle=3600,
        pool_timeout=30,
        pool_pre_ping=True
    )
)


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
        self.scoped_session = scoped_session(self.session_factory)

    def __enter__(self):
        self.session = self.scoped_session()
        return super().__enter__()

    def __del__(self):
        if self.scoped_session:
            self.scoped_session.remove()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
        self.scoped_session.remove()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def add(self, entity):
        self.session.add(entity)

    def add_all(self, *args):
        self.session.add_all([*args])

    @property
    def racks(self) -> RacksRepository:
        return RacksRepository(self.session)

    @property
    def devices(self) -> DevicesRepository:
        return DevicesRepository(self.session)
