#!/usr/bin/env python3
"""A module that contains the Cache class"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """A class that represent the caching mechanism"""

    def __init__(self):
        """Initialize the Cache class by creating a redis instance"""
        self._redis = redis.Redis()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store a new value in the database"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
