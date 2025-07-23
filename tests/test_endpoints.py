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
@pytest.mark.parametrize("invalid_payload", ["string", 123, [1, 2, 3], True, None])
def test_non_dict_payloads_rejected(endpoint: str, invalid_payload: Any):
    """Test that endpoints reject non-dict payloads with 422."""
    response = client.post(endpoint, json=invalid_payload)
    assert response.status_code == 422


@pytest.mark.parametrize("endpoint", ["/encrypt", "/decrypt", "/sign", "/verify"])
@pytest.mark.parametrize("invalid_content", ["invalid json", "{not valid json"])
def test_invalid_json_content_rejected(endpoint: str, invalid_content: str):
    """Test that endpoints reject invalid JSON content with 422."""
    response = client.post(
        endpoint, content=invalid_content, headers={"Content-Type": "application/json"}
    )
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
