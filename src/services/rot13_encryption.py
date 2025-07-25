import json
from typing import Any

from ..utils import to_deterministic_json
from .exceptions import DecryptionError
from .protocols import EncryptionProtocol


class ROT13EncryptionService(EncryptionProtocol):
    """
    ROT13-based encryption service implementation for demo purposes.
    https://en.wikipedia.org/wiki/ROT13
    """

    def encrypt(self, value: Any) -> str:
        """Encrypt a value using ROT13 encoding."""
        return self._rot13_encode(to_deterministic_json(value))

    def decrypt(self, encrypted_value: str) -> Any | None:
        """
        Decrypt a ROT13 encoded value.
        Returns None if the value cannot be decrypted.
        """
        try:
            return json.loads(self._rot13_decode(encrypted_value))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise DecryptionError(
                f"Failed to decrypt value: {encrypted_value!r} ({e})"
            ) from e

    def _rot13_encode(self, text: str) -> str:
        """Apply ROT13 encoding to text."""
        result: list[str] = []
        for char in text:
            if "a" <= char <= "z":
                result.append(chr((ord(char) - ord("a") + 13) % 26 + ord("a")))
            elif "A" <= char <= "Z":
                result.append(chr((ord(char) - ord("A") + 13) % 26 + ord("A")))
            else:
                result.append(char)
        return "".join(result)

    def _rot13_decode(self, text: str) -> str:
        """Decode ROT13 encoded text (ROT13 is its own inverse)."""
        return self._rot13_encode(text)  # symmetric 🧠
