from typing import Awaitable, Callable

from fastapi import HTTPException, Request, status
from fastapi.responses import Response


async def value_error_handler(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Middleware to catch ValueError exceptions and convert them to HTTP 400 responses.
    This eliminates the need for try-catch blocks in every endpoint.
    """
    try:
        return await call_next(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
