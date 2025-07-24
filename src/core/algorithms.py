from enum import StrEnum


class EncryptionAlgorithm(StrEnum):
    BASE64 = "base64"
    ROT13 = "rot13"


class SigningAlgorithm(StrEnum):
    HMAC = "hmac"
