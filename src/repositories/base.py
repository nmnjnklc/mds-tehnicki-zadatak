from typing import Generic, List, Optional, TypeVar, Union
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func, text, and_, or_
from sqlalchemy.sql.sqltypes import Boolean

from src.models.types.filter_by import FilterBy
from src.models.types.order_by import OrderBy


T = TypeVar("T")


class AbstractBaseRepository(ABC, Generic[T]):
    db_model = T

    @abstractmethod
    def add(self, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: Union[int, str], **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        quick_search: Optional[str] = None,
        filter_by: Optional[FilterBy] = None,
        order_by: Optional[OrderBy] = None,
    ) -> List[T]:
        raise NotImplementedError


class BaseRepository(AbstractBaseRepository[T]):
    def __init__(self, session: Session):
        self.session = session

    def add(self, **kwargs) -> T:
        db_entity = self.db_model(**kwargs)
        self.session.add(db_entity)
        self.session.flush()
        return db_entity

    def get(self, **kwargs) -> Optional[T]:
        return self.session.query(self.db_model).filter_by(**kwargs).first()

    def update(self, entity_id: Union[int, str], **kwargs):
        self.session.query(self.db_model).filter_by(id=entity_id).update(kwargs)

    def delete(self, **kwargs):
        self.session.query(self.db_model).filter_by(**kwargs).delete()

    def filter_query(
        self,
        query: Query,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        quick_search: Optional[str] = None,
        filter_by: Optional[FilterBy] = None,
        order_by: Optional[OrderBy] = None,
    ) -> List[T]:

        if filter_by:
            conditions = []

            for column, value in filter_by.items():
                sa_column = self.db_model.__table__.columns.get(column)

                if isinstance(value, list):
                    conditions.append(sa_column.in_(value))
                    continue

                if isinstance(sa_column.type, Boolean) and value in ["true", "false"]:
                    value = True if value == "true" else False

                conditions.append(sa_column == value)

            query = query.filter(and_(*conditions))

        if quick_search:
            conditions = []
            for column in self.db_model.__table__.columns:
                conditions.append(column.like(f"%{quick_search}%"))

            query = query.filter(or_(*conditions))

        if order_by:
            order_by_list = []
            for column, criteria in order_by.items():
                sa_column = self.db_model.__table__.columns.get(column)
                order_by_list.append(f"{sa_column} {criteria.value}")

            order_by_text = ", ".join(order_by_list)
            query = query.order_by(text(order_by_text))

        if page_size:
            query = query.limit(page_size)

        if page_number:
            query = query.offset((page_number - 1) * page_size)

        return query.all()

    def list(
        self,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        quick_search: Optional[str] = None,
        filter_by: Optional[FilterBy] = None,
        order_by: Optional[OrderBy] = None,
    ) -> List[T]:

        query = self.session.query(self.db_model)

        return self.filter_query(
            query=query,
            page_size=page_size,
            page_number=page_number,
            quick_search=quick_search,
            filter_by=filter_by,
            order_by=order_by
        )
