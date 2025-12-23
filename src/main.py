from fastapi import FastAPI
from contextlib import asynccontextmanager
from uvicorn import run

from src.routers import router
from src.exceptions import exception_handlers

from src.models.orm.base import create_db, run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Server starting
    create_db()
    run_migrations()
    yield
    # Server stopping


app: FastAPI = FastAPI(
    lifespan=lifespan,
    exception_handlers=exception_handlers
)

app.include_router(router=router)


if __name__ == "__main__":
    run(app=app)
