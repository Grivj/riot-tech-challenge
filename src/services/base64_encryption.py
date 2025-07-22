import base64
import json
from typing import Any

from .protocols import EncryptionProtocol


class Base64EncryptionService(EncryptionProtocol):
    """Base64-based encryption service implementation."""

    def encrypt(self, value: Any) -> str:
        """Encrypt a value using Base64 encoding."""
        # Convert to JSON string first, then encode
        json_str = json.dumps(value, separators=(",", ":"), sort_keys=True)
        return base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    def decrypt(self, encrypted_value: str) -> Any | None:
        """
        Decrypt a Base64 encoded value.
        Returns None if the value cannot be decrypted.
        """
        try:
            decoded_bytes = base64.b64decode(encrypted_value.encode("utf-8"))
            json_str = decoded_bytes.decode("utf-8")
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            return None

    def can_decrypt(self, value: str) -> bool:
        """Check if a string can be Base64 decoded and contains valid JSON."""
        return self.decrypt(value) is not None
