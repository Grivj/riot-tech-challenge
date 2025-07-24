from typing import Annotated

from fastapi import Header

from src.core.algorithms import EncryptionAlgorithm, SigningAlgorithm
from src.core.settings import settings
from src.services.base64_encryption import Base64EncryptionService
from src.services.encryption_service import EncryptionService
from src.services.hmac_signing import HMACSigningService
from src.services.rot13_encryption import ROT13EncryptionService
from src.services.signing_service import SigningService


class DependencyContainer:
    def __init__(self):
        # Initialize algorithm implementations
        self.encryption_algorithm = Base64EncryptionService()
        self.signing_algorithm = HMACSigningService(settings.HMAC_SECRET_KEY)

        # Initialize services
        self.encryption_service = EncryptionService(self.encryption_algorithm)
        self.signing_service = SigningService(self.signing_algorithm)


container = DependencyContainer()


def get_encryption_service(
    x_encryption_algorithm: Annotated[
        EncryptionAlgorithm, Header()
    ] = EncryptionAlgorithm.BASE64,
) -> EncryptionService:
    """
    Get encryption service based on algorithm specified in header.

    Supports:
    - base64: Base64 encoding (default)
    - rot13: ROT13 encoding (demo purpose 🧪)
    """

    match x_encryption_algorithm:
        case EncryptionAlgorithm.ROT13:
            algorithm = ROT13EncryptionService()
        case EncryptionAlgorithm.BASE64:
            algorithm = Base64EncryptionService()

    return EncryptionService(algorithm)


def get_signing_service(
    x_signing_algorithm: Annotated[SigningAlgorithm, Header()] = SigningAlgorithm.HMAC,
) -> SigningService:
    return container.signing_service
