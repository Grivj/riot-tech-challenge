from typing import Callable

from fastapi import HTTPException, Request, status
from fastapi.responses import Response


def value_error_handler(
    request: Request, call_next: Callable[[Request], Response]
) -> Response:
    """
    Middleware to catch ValueError exceptions and convert them to HTTP 400 responses.
    This eliminates the need for try-catch blocks in every endpoint.
    """
    try:
        return call_next(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
