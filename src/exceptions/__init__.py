from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from typing import Union

from fastapi.exceptions import RequestValidationError

from src.exceptions.base import (
    BaseError, ConflictError, BadRequestError, InternalServerError, EntityNotFound
)


def exception_handler(
    request: Request,
    exc: BaseError
) -> Union[JSONResponse, Response]:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


def data_validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Data validation error!", "details": exc.errors()}
    )


exception_handlers = {
    RequestValidationError: data_validation_exception_handler,

    ConflictError: exception_handler,
    BadRequestError: exception_handler,
    InternalServerError: exception_handler,
    EntityNotFound: exception_handler,
}
