from typing import Any, Protocol


class EncryptionProtocol(Protocol):
    """Protocol for encryption/decryption algorithms."""

    def encrypt(self, value: Any) -> str:
        """Encrypt a single value and return as string."""
        ...

    def decrypt(self, encrypted_value: str) -> Any | None:
        """
        Decrypt a string value back to its original type.
        Returns None if the value cannot be decrypted (not encrypted).
        """
        ...

    def can_decrypt(self, value: str) -> bool:
        """Check if a string value can be decrypted by this algorithm."""
        ...


class SigningProtocol(Protocol):
    """Protocol for signing and verification algorithms."""

    def sign(self, data: dict[str, Any]) -> str:
        """
        Generate a signature for the given data.
        The signature must be deterministic and order-independent for dict data.
        """
        ...

    def verify(self, data: dict[str, Any], signature: str) -> bool:
        """Verify if the signature matches the data."""
        ...
