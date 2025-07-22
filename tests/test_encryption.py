from src.services.base64_encryption import Base64EncryptionService
from src.services.encryption_service import EncryptionService


def test_base64_round_trip():
    """Test that encrypt -> decrypt returns original value."""
    service = Base64EncryptionService()

    test_cases = ["John Doe", 30, {"email": "test@example.com"}, [1, 2, 3], True, None]

    for original in test_cases:
        encrypted = service.encrypt(original)
        decrypted = service.decrypt(encrypted)
        assert decrypted == original


def test_can_decrypt_detection():
    """Test that can_decrypt correctly identifies encrypted vs unencrypted data."""
    service = Base64EncryptionService()

    # Valid encrypted data
    encrypted = service.encrypt("test")
    assert service.can_decrypt(encrypted) is True

    # Invalid data
    assert service.can_decrypt("1998-11-19") is False
    assert service.can_decrypt("not-base64") is False


def test_payload_encryption():
    """Test encrypting/decrypting full payloads."""
    algorithm = Base64EncryptionService()
    service = EncryptionService(algorithm)

    original = {
        "name": "John Doe",
        "age": 30,
        "contact": {"email": "john@example.com", "phone": "123-456-7890"},
    }

    # Encrypt
    encrypted = service.encrypt_payload(original)

    # All values should be strings (encrypted)
    for value in encrypted.values():
        assert isinstance(value, str)

    # Decrypt
    decrypted = service.decrypt_payload(encrypted)
    assert decrypted == original


def test_mixed_content_decryption():
    """Test decrypting payload with mixed encrypted/unencrypted content."""
    algorithm = Base64EncryptionService()
    service = EncryptionService(algorithm)

    # Mix of encrypted and unencrypted data
    payload = {
        "name": "IkpvaG4gRG9lIg==",  # encrypted "John Doe"
        "age": "MzA=",  # encrypted 30
        "birth_date": "1998-11-19",  # unencrypted
    }

    decrypted = service.decrypt_payload(payload)

    assert decrypted["name"] == "John Doe"
    assert decrypted["age"] == 30
    assert decrypted["birth_date"] == "1998-11-19"  # unchanged
