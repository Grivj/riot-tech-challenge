from src.services.hmac_signing import HMACSigningService
from src.services.signing_service import SigningService

EXTREMELY_SECRET_HMAC_SECRET = "extremely-secret-hmac-secret"


def test_signature_deterministic():
    """Test that signing the same data produces the same signature."""
    service = HMACSigningService(EXTREMELY_SECRET_HMAC_SECRET)

    data = {"message": "Hello World", "timestamp": 1616161616}
    signature1 = service.sign(data)
    signature2 = service.sign(data)

    assert signature1 == signature2


def test_signature_order_independent():
    """Test that property order doesn't affect signature."""
    service = HMACSigningService(EXTREMELY_SECRET_HMAC_SECRET)

    data1 = {"message": "Hello World", "timestamp": 1616161616}
    data2 = {"timestamp": 1616161616, "message": "Hello World"}

    signature1 = service.sign(data1)
    signature2 = service.sign(data2)

    assert signature1 == signature2


def test_signature_deep_nested_order_independent():
    """Test that key order in deeply nested objects doesn't affect signature."""
    service = HMACSigningService(EXTREMELY_SECRET_HMAC_SECRET)

    name = "John"
    age = 30
    address = {"city": "New York", "zip": 10001}

    data1 = {
        "user": {
            "name": name,
            "details": {"age": age, "address": address},
        }
    }
    # switched order of key-value pairs
    data2 = {
        "user": {
            "details": {"address": address, "age": age},
            "name": name,
        }
    }

    signature1 = service.sign(data1)
    signature2 = service.sign(data2)

    assert signature1 == signature2


def test_signature_verification():
    """Test basic signature verification."""
    service = HMACSigningService(EXTREMELY_SECRET_HMAC_SECRET)

    data = {"message": "Hello World", "timestamp": 1616161616}
    signature = service.sign(data)

    # Valid signature
    assert service.verify(data, signature) is True

    # Invalid signature
    assert service.verify(data, "invalid-signature") is False

    # Tampered data
    tampered_data = {"message": "Goodbye World", "timestamp": 1616161616}
    assert service.verify(tampered_data, signature) is False


def test_signing_service():
    """Test the signing service wrapper."""
    algorithm = HMACSigningService(EXTREMELY_SECRET_HMAC_SECRET)
    service = SigningService(algorithm)

    payload = {"message": "Hello World", "timestamp": 1616161616}

    # Sign
    result = service.sign_payload(payload)
    assert "signature" in result
    assert isinstance(result["signature"], str)

    # Verify
    signature = result["signature"]
    assert service.verify_payload(payload, signature) is True
    assert service.verify_payload(payload, "invalid") is False
