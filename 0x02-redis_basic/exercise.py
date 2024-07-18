#!/usr/bin/env python3
"""A module that contains the Cache class"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count number of method calls"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A wrapper around methods to count number of method calls"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """A class that represent the caching mechanism"""

    def __init__(self):
        """Initialize the Cache class by creating a redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store a new value in the database"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """Get the value associated with this key in the database"""
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Parametrize Cache.get with the str function"""
        return self._redis.get(key, str).decode("utf-8")

    def get_int(self, key: str) -> int:
        """Parametrize Cache.get with the int function"""
        return self._redis.get(key, int)
