from fastapi import APIRouter

from src.routers.racks import racks_router
from src.routers.devices import devices_router
from src.routers.balancer import balancer_router


router: APIRouter = APIRouter(prefix="/api")

router.include_router(router=balancer_router)
router.include_router(router=racks_router)
router.include_router(router=devices_router)
