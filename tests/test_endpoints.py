"""Basic endpoint tests for error cases and validation."""

from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health endpoint works."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("endpoint", ["/encrypt", "/decrypt", "/sign", "/verify"])
@pytest.mark.parametrize(
    "invalid_payload,content_type",
    [
        # Non-dict payloads
        ("string", "application/json"),
        (123, "application/json"),
        ([1, 2, 3], "application/json"),
        (True, "application/json"),
        (None, "application/json"),
        # Invalid JSON
        ("invalid json", "application/json"),
        ("{not valid json", "application/json"),
    ],
)
def test_invalid_payloads_rejected(
    endpoint: str, invalid_payload: Any, content_type: str
):
    """Test that endpoints reject invalid payloads with 422."""
    if isinstance(invalid_payload, str) and "json" in invalid_payload:
        # For invalid JSON strings, send as raw content
        response = client.post(
            endpoint, content=invalid_payload, headers={"Content-Type": content_type}
        )
    else:
        # For other invalid types, let FastAPI serialize them
        response = client.post(endpoint, json=invalid_payload)

    assert response.status_code == 422


def test_empty_payloads():
    """Test handling of empty payloads."""
    # Empty dict should work
    response = client.post("/encrypt", json={})
    assert response.status_code == 200
    assert response.json() == {}

    response = client.post("/decrypt", json={})
    assert response.status_code == 200
    assert response.json() == {}

    response = client.post("/sign", json={})
    assert response.status_code == 200
    assert "signature" in response.json()


@pytest.mark.parametrize("payload", [{"signature": "test"}, {"data": {}}])
def test_verify_endpoint_validation(payload: dict[str, Any]):
    """Test verify endpoint requires correct structure."""
    response = client.post("/verify", json=payload)
    assert response.status_code == 422
