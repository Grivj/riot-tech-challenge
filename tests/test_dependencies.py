from src.core.algorithms import EncryptionAlgorithm
from src.core.dependencies import get_encryption_service
from src.services.base64_encryption import Base64EncryptionService
from src.services.encryption_service import EncryptionService
from src.services.rot13_encryption import ROT13EncryptionService


def test_get_encryption_service_default():
    """Test that get_encryption_service returns Base64 by default."""
    service = get_encryption_service()

    assert isinstance(service, EncryptionService)
    assert isinstance(service.algorithm, Base64EncryptionService)


def test_get_encryption_service_base64():
    """Test that get_encryption_service returns Base64 when specified."""
    service = get_encryption_service(EncryptionAlgorithm.BASE64)

    assert isinstance(service, EncryptionService)
    assert isinstance(service.algorithm, Base64EncryptionService)


def test_get_encryption_service_rot13():
    """Test that get_encryption_service returns ROT13 when specified."""
    service = get_encryption_service(EncryptionAlgorithm.ROT13)

    assert isinstance(service, EncryptionService)
    assert isinstance(service.algorithm, ROT13EncryptionService)
