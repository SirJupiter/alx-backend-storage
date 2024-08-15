#!/usr/bin/env python3
"""Redis caching"""

import redis
from uuid import uuid4
from typing import Union


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
