from typing import Any

from pydantic import BaseModel


class SignatureResponse(BaseModel):
    """Response model for signing operations."""

    signature: str


class VerificationRequest(BaseModel):
    """Request model for signature verification."""

    signature: str
    data: dict[str, Any]
