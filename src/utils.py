import json
from typing import Any


def to_deterministic_json(data: Any) -> str:
    """
    Convert data to a deterministic JSON string representation.

    Uses compact formatting and sorted keys to ensure consistent output
    regardless of input order. Used for signing to ensure order independence.
    """
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def to_compact_json(data: Any) -> str:
    """
    Convert data to a compact JSON string representation.

    Uses compact formatting but preserves original key order.
    Used for encryption where order independence is not required.
    """
    return json.dumps(data, separators=(",", ":"))
