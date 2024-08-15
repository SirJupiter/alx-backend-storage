#!/usr/bin/env python3
"""Redis caching"""

import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a function is called

    Args:
        method: function to count

    Returns:
        Callable: function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache():
    """Class contains Redis operations

    Attributes:
        client: Redis client
        store: Redis store
    """
    def __init__(self):
        """Instantiation function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis

        Args:
            data: data to store

        Returns:
            str: key
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """Converts data value of key back to desired format

        Args:
            key: key of data stored
            fn: function that does the conversion

        Returns:
            Union[str, bytes, int, float]: data
        """
        value = self._redis.get(key)

        if value and fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """Converts data value of key back to string

        Args:
            key: key of data stored

        Returns:
            str: data
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Converts data value of key back to int

        Args:
            key: key of data stored

        Returns:
            int: data
        """
        return self.get(key, int)
