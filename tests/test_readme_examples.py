"""Tests for exact examples from the README."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_encrypt_readme_example():
    """Test the exact encryption example from README."""
    payload = {
        "name": "John Doe",
        "age": 30,
        "contact": {"email": "john@example.com", "phone": "123-456-7890"},
    }

    response = client.post("/encrypt", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "IkpvaG4gRG9lIg=="
    assert data["age"] == "MzA="
    assert (
        data["contact"]
        == "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9"
    )


def test_decrypt_readme_example():
    """Test the exact decryption example from README."""
    payload = {
        "name": "IkpvaG4gRG9lIg==",
        "age": "MzA=",
        "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9",
    }

    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200

    expected = {
        "name": "John Doe",
        "age": 30,
        "contact": {"email": "john@example.com", "phone": "123-456-7890"},
    }
    assert response.json() == expected


def test_decrypt_mixed_content_readme_example():
    """Test the mixed content decryption example from README."""
    payload = {
        "name": "IkpvaG4gRG9lIg==",
        "age": "MzA=",
        "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9",
        "birth_date": "1998-11-19",
    }

    response = client.post("/decrypt", json=payload)
    assert response.status_code == 200

    expected = {
        "name": "John Doe",
        "age": 30,
        "contact": {"email": "john@example.com", "phone": "123-456-7890"},
        "birth_date": "1998-11-19",
    }
    assert response.json() == expected


def test_sign_order_independence():
    """Test that property order doesn't affect signature (README requirement)."""
    payload1 = {"message": "Hello World", "timestamp": 1616161616}
    payload2 = {"timestamp": 1616161616, "message": "Hello World"}

    response1 = client.post("/sign", json=payload1)
    response2 = client.post("/sign", json=payload2)

    assert response1.status_code == 200
    assert response2.status_code == 200

    signature1 = response1.json()["signature"]
    signature2 = response2.json()["signature"]

    assert signature1 == signature2


def test_verify_valid_signature():
    """Test verifying a valid signature (README flow)."""
    data = {"message": "Hello World", "timestamp": 1616161616}

    # Sign
    sign_response = client.post("/sign", json=data)
    signature = sign_response.json()["signature"]

    # Verify
    verify_payload = {"signature": signature, "data": data}
    response = client.post("/verify", json=verify_payload)

    assert response.status_code == 204


def test_verify_invalid_signature():
    """Test verifying invalid signature returns 400 (README requirement)."""
    verify_payload = {
        "signature": "a1b2c3d4e5f6g7h8i9j0...",
        "data": {"timestamp": 1616161616, "message": "Goodbye World"},
    }

    response = client.post("/verify", json=verify_payload)
    assert response.status_code == 400


def test_encrypt_decrypt_consistency():
    """Test that /encrypt followed by /decrypt returns original (README requirement)."""
    original = {
        "name": "John Doe",
        "age": 30,
        "contact": {"email": "john@example.com", "phone": "123-456-7890"},
    }

    # Encrypt
    encrypt_response = client.post("/encrypt", json=original)
    encrypted = encrypt_response.json()

    # Decrypt
    decrypt_response = client.post("/decrypt", json=encrypted)
    decrypted = decrypt_response.json()

    assert decrypted == original


def test_sign_verify_consistency():
    """Test that /sign followed by /verify works (README requirement)."""
    payload = {"message": "Hello World", "timestamp": 1616161616}

    # Sign
    sign_response = client.post("/sign", json=payload)
    signature = sign_response.json()["signature"]

    # Verify
    verify_payload = {"signature": signature, "data": payload}
    verify_response = client.post("/verify", json=verify_payload)

    assert verify_response.status_code == 204
