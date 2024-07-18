#!/usr/bin/env python3
"""A module that contains the Cache class"""
import redis
import requests
from functools import wraps
from typing import Callable
from datetime import timedelta


def cache(fn: Callable) -> Callable:
    """Cache the get requests"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        """A wrapper to cache the result of get equests"""
        url = args[0]
        r = redis.Redis()
        r.incr(f'count:{url}')
        content = r.get('content: url')
        if content:
            return content.decode('utf-8')
        res = fn(*args, **kwargs)
        r.set('content: url', res)
        r.set(f'count:{url}', 1)
        r.expire(f'content:{url}', timedelta(seconds=10))
        return res
    return wrapper


@cache
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and returns it"""
    res = requests.get(url)
    return res.content.decode('utf-8')
