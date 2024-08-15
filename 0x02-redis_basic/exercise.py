#!/usr/bin/env python3
"""Redis caching"""

import redis
from uuid import uuid4
from typing import Union, Callable, Any
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


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


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

    @call_history
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
