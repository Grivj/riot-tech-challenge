from dataclasses import dataclass
from typing import Any

from .protocols import SigningProtocol


@dataclass(frozen=True)
class SigningService:
    """Service for signing and verifying JSON payloads."""

    algorithm: SigningProtocol

    def sign_payload(self, payload: dict[str, Any]) -> dict[str, str]:
        """
        Sign a payload and return the signature.
        Returns a dictionary with only the signature.

        Example:
            >>> service = SigningService(HMACSigningService())
            >>> service.sign_payload({"name": "John Doe", "age": 30})
            {"signature": "sha256=..."}
        """
        return {"signature": self.algorithm.sign(payload)}

    def verify_payload(self, data: dict[str, Any], signature: str) -> bool:
        """Verify if the signature matches the data.

        Example:
            >>> service = SigningService(HMACSigningService())
            >>> service.verify_payload({"name": "John Doe", "age": 30}, "sha256=...")
            True
        """
        return self.algorithm.verify(data, signature)
