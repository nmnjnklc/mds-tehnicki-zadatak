from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.services import balancer

from src.exceptions.base import InternalServerError


balancer_router: APIRouter = APIRouter(prefix="/balancer", tags=["Rack energy balancer"])


@balancer_router.get(path="/balance-rack-energy-consumption")
def balance_rack_energy_consumption(request: Request) -> JSONResponse:
    balancer.balance()
    return JSONResponse(content={"message": "OK"}, status_code=status.HTTP_200_OK)
