from typing import Any

from fastapi import HTTPException
from starlette import status

from seedwork.domain.errors import ErrorType

STATUS_CODES = {
    ErrorType.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorType.CONFLICT: status.HTTP_409_CONFLICT,
    ErrorType.VALIDATION: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ErrorType.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    ErrorType.SYSTEM: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def handle_errors(
    result: Any,
    error_types: list | None = None,
    status_codes: dict[ErrorType, int] | None = None,
) -> None:
    assert error_types, "Please pass the errors being processed."
    status_codes = status_codes or STATUS_CODES

    if result.error and result.error.type in error_types:
        raise HTTPException(
            status_code=status_codes[result.error.type],
            detail=result.error.detail,
        )
