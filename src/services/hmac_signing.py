import hashlib
import hmac
from typing import Any

from ..utils import to_deterministic_json
from .protocols import SigningProtocol


class HMACSigningService(SigningProtocol):
    """HMAC-based signing service implementation."""

    def __init__(self, secret_key: str):
        """Initialize with a secret key for HMAC."""
        self.secret_key = secret_key.encode("utf-8")

    def sign(self, data: dict[str, Any]) -> str:
        """
        Generate an HMAC signature for the given data.
        Uses deterministic JSON serialization to ensure order independence.

        Example:
            >>> service = HMACSigningService()
            >>> service.sign({"name": "John Doe", "age": 30})
            "sha256=..."
        """
        return hmac.new(
            self.secret_key,
            to_deterministic_json(data).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def verify(self, data: dict[str, Any], signature: str) -> bool:
        """Verify if the signature matches the data."""
        expected_signature = self.sign(data)
        return hmac.compare_digest(signature, expected_signature)
