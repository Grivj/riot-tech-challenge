"""Tests for utility functions."""

from typing import Any

import pytest

from src.utils import to_deterministic_json


@pytest.mark.parametrize(
    "data,expected",
    [
        ({"name": "John", "age": 30}, '{"age":30,"name":"John"}'),
        ({"b": 2, "a": 1}, '{"a":1,"b":2}'),
        ([1, 2, 3], "[1,2,3]"),
        ("test", '"test"'),
        (123, "123"),
        (True, "true"),
        (None, "null"),
    ],
)
def test_to_deterministic_json_format(data: Any, expected: str):
    """Test that to_deterministic_json produces expected compact format."""
    result = to_deterministic_json(data)
    assert result == expected


def test_to_deterministic_json_order_independence():
    """Test that property order doesn't affect output."""
    data1 = {"name": "John", "age": 30, "city": "NYC"}
    data2 = {"city": "NYC", "name": "John", "age": 30}
    data3 = {"age": 30, "city": "NYC", "name": "John"}

    result1 = to_deterministic_json(data1)
    result2 = to_deterministic_json(data2)
    result3 = to_deterministic_json(data3)

    assert result1 == result2 == result3
    assert result1 == '{"age":30,"city":"NYC","name":"John"}'


def test_to_deterministic_json_nested_objects():
    """Test that nested objects are also sorted deterministically."""
    data1 = {
        "user": {"name": "John", "age": 30},
        "settings": {"theme": "dark", "lang": "en"},
    }
    data2 = {
        "settings": {"lang": "en", "theme": "dark"},
        "user": {"age": 30, "name": "John"},
    }

    result1 = to_deterministic_json(data1)
    result2 = to_deterministic_json(data2)

    assert result1 == result2
    assert (
        result1
        == '{"settings":{"lang":"en","theme":"dark"},"user":{"age":30,"name":"John"}}'
    )
