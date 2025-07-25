from typing import Any

import pytest

from src.services.base64_encryption import Base64EncryptionService
from src.services.encryption_service import EncryptionService


@pytest.mark.parametrize(
    "original",
    [
        "John Doe",
        30,
        {"email": "test@example.com"},
        [1, 2, 3],
        True,
        None,
    ],
)
def test_base64_round_trip(original: Any):
    """Test that encrypt -> decrypt returns original value."""
    service = Base64EncryptionService()

    encrypted = service.encrypt(original)
    decrypted = service.decrypt(encrypted)
    assert decrypted == original


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
    assert len(encrypted) == 3
    assert "name" in encrypted and isinstance(encrypted["name"], str)
    assert "age" in encrypted and isinstance(encrypted["age"], str)
    assert "contact" in encrypted and isinstance(encrypted["contact"], str)

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


def test_none_value_preservation():
    """Test that original None values are preserved after encrypt/decrypt cycle."""
    algorithm = Base64EncryptionService()
    service = EncryptionService(algorithm)

    original = {
        "name": "John",
        "value": None,
        "active": True,
        "second_level": {"age": 25, "occupation": None},
    }

    encrypted = service.encrypt_payload(original)
    assert all(isinstance(v, str) for v in encrypted.values())

    decrypted = service.decrypt_payload(encrypted)

    # None value should be perfectly preserved
    assert decrypted == original
    assert decrypted["value"] is None
    assert type(decrypted["value"]) is type(None)
    assert decrypted["second_level"]["occupation"] is None
