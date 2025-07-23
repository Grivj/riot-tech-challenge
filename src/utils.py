import json
from typing import Any


def to_deterministic_json(data: Any) -> str:
    """
    Convert data to a deterministic JSON string representation.
    (that works for nested objects too 🪆)

    Uses compact formatting and sorted keys to ensure consistent output
    regardless of input order or formatting.

    Example:
        >>> to_deterministic_json({"name": "John", "age": 30})
        '{"age":30,"name":"John"}'
        >>> to_deterministic_json(
            {
                "name": "John",
                "age": 30,
                "contact": {"email": "test@example.com", "phone": "123-456-7890"},
            }
        )
        '{"age":30,"contact":{"email":"test@example.com","phone":"123-456-7890"},"name":"John"}'
    """
    return json.dumps(data, separators=(",", ":"), sort_keys=True)
