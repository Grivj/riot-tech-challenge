from dataclasses import dataclass


@dataclass
class DecryptionError(Exception):
    message: str
