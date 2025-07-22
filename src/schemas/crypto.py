from typing import Any

from pydantic import BaseModel, Field


class SignatureResponse(BaseModel):
    """Response model for signing operations."""

    signature: str = Field(
        ...,
        description="HMAC-SHA256 signature of the input data",
        examples=[
            "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
        ],
    )


class VerificationRequest(BaseModel):
    """Request model for signature verification."""

    signature: str = Field(
        ...,
        description="The signature to verify against the data",
        examples=[
            "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6",
        ],
    )
    data: dict[str, Any] = Field(
        ...,
        description="The data object that was originally signed",
        examples=[
            {"message": "Hello World", "timestamp": 1616161616, "user_id": 123},
        ],
    )
