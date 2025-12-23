from fastapi import status
from typing import Union, Optional

from sqlalchemy.exc import IntegrityError


class BaseError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class ConflictError(BaseError):
    def __init__(self, exc: Union[IntegrityError, Exception, None] = None):

        message: str = "Database integrity error"

        if isinstance(exc, IntegrityError):
            message: str = exc.orig.args[1]    \
                            .split(": ")[1]    \
                            .replace("'", "")  \
                            .replace(".", " ") \
                            .replace("key ", "")

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"Conflict: {message}!"
        )


class BadRequestError(BaseError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Bad request!"
        )


class InternalServerError(BaseError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error!"
        )


class EntityNotFound(BaseError):
    def __init__(self, entity_name: Optional[str] = "Entity"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{entity_name} not found."
        )
