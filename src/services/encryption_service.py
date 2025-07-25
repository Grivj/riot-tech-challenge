from dataclasses import dataclass
from typing import Any

from .exceptions import DecryptionError
from .protocols import EncryptionProtocol


@dataclass(frozen=True)
class EncryptionService:
    """Service for encrypting and decrypting JSON payloads."""

    algorithm: EncryptionProtocol

    def encrypt_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Encrypt all properties at depth 1 in the payload.
        Returns a new dictionary with encrypted values.
        """

        return {key: self.algorithm.encrypt(value) for key, value in payload.items()}

    def decrypt_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Decrypt properties in the payload that can be decrypted.
        Non-encrypted properties remain unchanged.
        Returns a new dictionary with decrypted values where possible.

        Example:
            >>> service = EncryptionService(Base64EncryptionService())
            >>> service.decrypt_payload({"name": "IkpvaG4gRG9lIg==", "age": "MzA="})
            {"name": "John Doe", "age": 30}
        """

        result: dict[str, Any] = {}
        for key, value in payload.items():
            if isinstance(value, str):
                # we can try to decrypt
                try:
                    result[key] = self.algorithm.decrypt(value)
                except DecryptionError:
                    # unable to decrypt, keep as-is
                    result[key] = value
            else:
                # not a string, keep as-is
                result[key] = value
        return result
