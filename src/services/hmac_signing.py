import hashlib
import hmac
import json
from typing import Any

from .protocols import SigningProtocol


class HMACSigningService(SigningProtocol):
    """HMAC-based signing service implementation."""

    def __init__(self, secret_key: str):
        """Initialize with a secret key for HMAC."""
        self.secret_key = secret_key.encode("utf-8")

    def sign(self, data: Any) -> str:
        """
        Generate an HMAC signature for the given data.
        Uses deterministic JSON serialization to ensure order independence.

        Example:
            >>> service = HMACSigningService()
            >>> service.sign({"name": "John Doe", "age": 30})
            "sha256=..."
        """
        # Create deterministic(sorted by key) JSON representation
        json_str = json.dumps(data, sort_keys=True)

        return hmac.new(
            self.secret_key, json_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def verify(self, data: Any, signature: str) -> bool:
        """Verify if the signature matches the data."""
        expected_signature = self.sign(data)
        return hmac.compare_digest(signature, expected_signature)
