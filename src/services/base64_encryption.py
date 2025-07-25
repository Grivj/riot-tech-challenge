import base64
import binascii
import json
from typing import Any

from ..utils import to_deterministic_json
from .exceptions import DecryptionError
from .protocols import EncryptionProtocol


class Base64EncryptionService(EncryptionProtocol):
    """Base64-based encryption service implementation."""

    def encrypt(self, value: Any) -> str:
        """Encrypt a value using Base64 encoding."""
        return base64.b64encode(to_deterministic_json(value).encode("utf-8")).decode(
            "utf-8"
        )

    def decrypt(self, encrypted_value: str) -> Any:
        """
        Decrypt a Base64 encoded value.
        Raises DecryptionError if the value cannot be decrypted.
        """
        try:
            decoded_bytes = base64.b64decode(encrypted_value.encode("utf-8"))
            json_str = decoded_bytes.decode("utf-8")
            return json.loads(json_str)
        except (ValueError, json.JSONDecodeError, binascii.Error) as e:
            raise DecryptionError(
                f"Failed to decrypt value: {encrypted_value!r} ({e})"
            ) from e
