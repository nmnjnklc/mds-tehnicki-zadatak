from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.models.types.order_by import Order
from src.models.domain.rack import (
    Rack, RackCreate, RackUpdate, RackDetails
)

from src.services import racks_service

from src.exceptions.base import (
    EntityNotFound, ConflictError, InternalServerError
)


racks_router: APIRouter = APIRouter(prefix="/racks", tags=["Racks"])


@racks_router.post(path="/list", response_model=list[Rack])
def get_all_racks(
        request: Request,
        quick_search: Optional[str] = None,
        order_type: Order = Order.ASCENDING,
        order_by: Optional[str] = "id",
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        filter_by: Optional[dict] = None,
) -> JSONResponse:
    racks = racks_service.list_ordered_by(
        quick_search=quick_search,
        order_type=order_type,
        order_by=order_by,
        page_size=page_size,
        page_number=page_number,
        filter_by=filter_by
    )
    return JSONResponse(content=[rack.model_dump() for rack in racks], status_code=status.HTTP_200_OK)


@racks_router.get(path="/get/{rack_id}", response_model=Rack)
def get_rack(request: Request, rack_id: int) -> JSONResponse:
    rack = racks_service.get(id=rack_id)
    if not rack:
        raise EntityNotFound(entity_name="Rack")
    return JSONResponse(content=rack.model_dump(), status_code=status.HTTP_200_OK)


@racks_router.get(path="/get/details/{rack_id}", response_model=RackDetails)
def get_rack_details(request: Request, rack_id: int) -> JSONResponse:
    rack: RackDetails = racks_service.get_rack_details(rack_id=rack_id)
    if not rack:
        raise EntityNotFound(entity_name="Rack")
    return JSONResponse(content=rack[0].model_dump(), status_code=status.HTTP_200_OK)


@racks_router.get(path="/list/details", response_model=list[RackDetails])
def get_all_racks_details(request: Request) -> JSONResponse:
    racks: list[RackDetails] = racks_service.get_rack_details()
    return JSONResponse(content=[rack.model_dump() for rack in racks], status_code=status.HTTP_200_OK)


@racks_router.post(path="/create")
def create_rack(request: Request, rack: RackCreate) -> JSONResponse:
    try:
        racks_service.create(**rack.model_dump())
    except IntegrityError:
        raise ConflictError
    except Exception:
        raise InternalServerError
    return JSONResponse(content={"message": "Rack successfully created."}, status_code=status.HTTP_201_CREATED)


@racks_router.put(path="/update/{rack_id}")
def update_rack(request: Request, rack_id: int, rack: RackUpdate) -> JSONResponse:
    try:
        racks_service.update(entity_id=rack_id, **rack.model_dump())
    except IntegrityError:
        raise ConflictError
    except Exception:
        raise InternalServerError
    return JSONResponse(content={"message": "Rack updated successfully."}, status_code=status.HTTP_200_OK)


@racks_router.delete(path="/delete/{rack_id}")
def delete_rack(request: Request, rack_id: int) -> JSONResponse:
    racks_service.delete(entity_id=rack_id)
    return JSONResponse(content={"message": "Rack deleted successfully."}, status_code=status.HTTP_200_OK)
