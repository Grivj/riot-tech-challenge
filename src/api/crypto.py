from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from src.core.dependencies import get_encryption_service, get_signing_service
from src.schemas.crypto import SignatureResponse, VerificationRequest
from src.services.encryption_service import EncryptionService
from src.services.signing_service import SigningService

router = APIRouter(tags=["crypto"])


@router.post(
    "/encrypt",
    summary="Encrypt JSON payload",
    description="Encrypts all properties at depth 1 of the input JSON payload using Base64 encoding.",
    response_description="JSON object with all top-level properties encrypted as strings",
)
async def encrypt_payload(
    payload: dict[str, Any],
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> dict[str, Any]:
    """
    Encrypt all properties at depth 1 of the input payload.

    The endpoint encrypts each top-level property individually, so nested objects
    are encrypted as complete units. Returns a new JSON object where all values
    are Base64-encoded strings.
    """
    return encryption_service.encrypt_payload(payload)


@router.post(
    "/decrypt",
    summary="Decrypt JSON payload",
    description="Decrypts properties that can be decrypted, leaves others unchanged.",
    response_description="JSON object with decrypted values where possible",
)
async def decrypt_payload(
    payload: dict[str, Any],
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> dict[str, Any]:
    """
    Decrypt properties in the payload that can be decrypted.

    Only attempts to decrypt string values that are valid Base64-encoded JSON.
    Non-encrypted properties remain unchanged, allowing for mixed content.
    """
    return encryption_service.decrypt_payload(payload)


@router.post(
    "/sign",
    response_model=SignatureResponse,
    summary="Generate signature",
    description="Generates an HMAC-SHA256 signature for the input data.",
    response_description="Object containing the generated signature",
)
async def sign_payload(
    payload: dict[str, Any],
    signing_service: SigningService = Depends(get_signing_service),
) -> SignatureResponse:
    """
    Generate a signature for the input payload.

    Uses HMAC-SHA256 with deterministic JSON serialization to ensure the same
    signature is generated regardless of property order in the input object.
    """
    result = signing_service.sign_payload(payload)
    return SignatureResponse(**result)


@router.post(
    "/verify",
    summary="Verify signature",
    description="Verifies if a signature matches the provided data.",
    responses={
        204: {"description": "Signature is valid"},
        400: {"description": "Signature is invalid or malformed"},
    },
)
async def verify_signature(
    request: VerificationRequest,
    signing_service: SigningService = Depends(get_signing_service),
) -> Response:
    """
    Verify a signature against the provided data.

    Returns HTTP 204 (No Content) if the signature is valid,
    or HTTP 400 (Bad Request) if the signature is invalid or doesn't match.

    The verification is order-independent - the same signature will validate
    regardless of the order of properties in the data object.
    """
    if not signing_service.verify_payload(request.data, request.signature):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
