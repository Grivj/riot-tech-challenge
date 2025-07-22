from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from src.core.dependencies import get_encryption_service, get_signing_service
from src.schemas.crypto import SignatureResponse, VerificationRequest
from src.services.encryption_service import EncryptionService
from src.services.signing_service import SigningService

router = APIRouter(tags=["crypto"])


@router.post("/encrypt")
async def encrypt_payload(
    payload: dict[str, Any],
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> dict[str, Any]:
    """Encrypt all properties at depth 1 of the input payload."""
    try:
        return encryption_service.encrypt_payload(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/decrypt")
async def decrypt_payload(
    payload: dict[str, Any],
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> dict[str, Any]:
    """
    Decrypt properties in the payload that can be decrypted.
    Non-encrypted properties remain unchanged.
    """
    try:
        return encryption_service.decrypt_payload(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sign", response_model=SignatureResponse)
async def sign_payload(
    payload: dict[str, Any],
    signing_service: SigningService = Depends(get_signing_service),
) -> SignatureResponse:
    """Generate a signature for the input payload."""
    try:
        result = signing_service.sign_payload(payload)
        return SignatureResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/verify")
async def verify_signature(
    request: VerificationRequest,
    signing_service: SigningService = Depends(get_signing_service),
) -> Response:
    """
    Verify a signature against the provided data.
    Returns 204 if valid, 400 if invalid.
    """
    try:
        if not signing_service.verify_payload(request.data, request.signature):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
