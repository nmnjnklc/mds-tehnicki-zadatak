from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.models.types.order_by import Order
from src.models.domain.device import (
    Device, DeviceCreate, DeviceUpdate, DeviceAssignment
)

from src.services import devices_service

from src.exceptions.base import (
    EntityNotFound, ConflictError, InternalServerError
)


devices_router: APIRouter = APIRouter(prefix="/devices", tags=["Devices"])


@devices_router.get(path="/get/{device_id}", response_model=Device)
def get_device(request: Request, device_id: int) -> JSONResponse:
    device = devices_service.get(id=device_id)
    if not device:
        raise EntityNotFound(entity_name="Device")
    return JSONResponse(content=device.model_dump(), status_code=status.HTTP_200_OK)


@devices_router.post(path="/list", response_model=list[Device])
def get_all_devices(
        request: Request,
        quick_search: Optional[str] = None,
        order_type: Order = Order.ASCENDING,
        order_by: Optional[str] = "id",
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
        filter_by: Optional[dict] = None,
) -> JSONResponse:
    devices = devices_service.list_ordered_by(
        quick_search=quick_search,
        order_type=order_type,
        order_by=order_by,
        page_size=page_size,
        page_number=page_number,
        filter_by=filter_by
    )
    return JSONResponse(content=[device.model_dump() for device in devices], status_code=status.HTTP_200_OK)


@devices_router.post(path="/create")
def create_device(request: Request, device: DeviceCreate) -> JSONResponse:
    try:
        devices_service.create(**device.model_dump())
    except IntegrityError:
        raise ConflictError
    except Exception:
        raise InternalServerError
    return JSONResponse(content={"message": "Device created successfully."}, status_code=status.HTTP_201_CREATED)


@devices_router.patch(path="/assign")
def assign_device_to_rack(request: Request, assignment: DeviceAssignment) -> JSONResponse:
    try:
        devices_service.update(entity_id=assignment.device_id, rack_id=assignment.rack_id)
    except IntegrityError:
        raise ConflictError
    except Exception:
        raise InternalServerError
    return JSONResponse(content={"message": "Device assigned successfully to rack."}, status_code=status.HTTP_200_OK)


@devices_router.put(path="/update/{device_id}")
def update_device(request: Request, device_id: int, device: DeviceUpdate) -> JSONResponse:
    try:
        devices_service.update(entity_id=device_id, **device.model_dump())
    except IntegrityError:
        raise ConflictError
    except Exception:
        raise InternalServerError
    return JSONResponse(content={"message": "Device updated successfully."}, status_code=status.HTTP_200_OK)


@devices_router.delete(path="/delete/{device_id}")
def delete_device(request: Request, device_id: int) -> JSONResponse:
    devices_service.delete(entity_id=device_id)
    return JSONResponse(content={"message": "Device deleted successfully."}, status_code=status.HTTP_200_OK)
