from typing import Any, Protocol


class EncryptionProtocol(Protocol):
    """Protocol for encryption/decryption algorithms."""

    def encrypt(self, value: Any) -> str:
        """Encrypt a single value and return as string."""
        ...

    def decrypt(self, encrypted_value: str) -> Any:
        """
        Decrypt a string value back to its original type.
        Raises DecryptionError if the value cannot be decrypted.
        """
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
