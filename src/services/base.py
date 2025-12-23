from typing import Generic, List, TypeVar, Optional
from abc import ABC

from src.repositories.uow import AbstractUnitOfWork
from src.models.types.order_by import Order


T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        domain_model_type: T,
        repository_name: str,
    ):
        self.uow = uow
        self.repository_name = repository_name
        self.domain_model_type = domain_model_type

    @property
    def repository(self):
        return getattr(self.uow, self.repository_name, None)

    def get(self, **kwargs) -> T:
        with self.uow:
            db_entity = self.repository.get(**kwargs)
            if not db_entity:
                return None
            return self.domain_model_type.model_validate(db_entity)

    def list_ordered_by(
            self,
            filter_by: dict,
            order_type: Order = Order.ASCENDING,
            order_by: Optional[str] = "id",
            quick_search: Optional[str] = None,
            page_size: Optional[int] = None,
            page_number: Optional[int] = None
    ) -> List[T]:
        with self.uow:
            entities = self.repository.list(
                filter_by=filter_by,
                quick_search=quick_search,
                page_size=page_size,
                page_number=page_number,
                order_by={order_by: order_type}
            )
            return [self.domain_model_type.model_validate(e) for e in entities]

    def list(self) -> List[T]:
        with self.uow:
            entities = self.repository.list()
            return [self.domain_model_type.model_validate(e) for e in entities]

    def create(self, **kwargs):
        with self.uow:
            self.repository.add(**kwargs)
            self.uow.commit()

    def update(self, entity_id: int, **kwargs) -> bool:
        with self.uow:
            if not self.repository.get(id=entity_id):
                return False
            self.repository.update(entity_id, **kwargs)
            self.uow.commit()
            return True

    def delete(self, entity_id: int) -> bool:
        with self.uow:
            if not self.repository.get(id=entity_id):
                return False
            self.repository.delete(id=entity_id)
            self.uow.commit()
            return True
