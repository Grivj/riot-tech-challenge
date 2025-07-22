from src.core.settings import settings
from src.services.base64_encryption import Base64EncryptionService
from src.services.encryption_service import EncryptionService
from src.services.hmac_signing import HMACSigningService
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


def get_encryption_service() -> EncryptionService:
    # TODO: Could extend with multiple encryption algorithms
    # and select the one to use via query param or header
    # then strategy pattern ✨
    return container.encryption_service


def get_signing_service() -> SigningService:
    # TODO: Could extend with multiple signing algorithms
    # and select the one to use via query param or header
    # then strategy pattern ✨
    return container.signing_service
