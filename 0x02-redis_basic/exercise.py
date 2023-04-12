#!/usr/bin/env python3
"""Writing strings to Redis"""


import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that increments a key with the method's name in Redis
    every time it's called
    """
    @wraps(method)
    def wrapper(*args, **kwargs):

        key = method.__qualname__
        args[0]_redis.incr(key)
        return method(*args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history
    for a particular function in Redis
    """
    @wraps(method)
    def wrapper(*args, **kwargs):

        key = method.__qualname__
        args[0]_redis.rpush(f'{key}:inputs', str(args[1:]))
        output = method(*args, **kwargs)
        args[0]_redis.rpush(f'{key}:outputs', str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Prints the call history of the method passed as a parameter
    """
    red = redis.Redis()
    key = method.__qualname__
    method_count = red.get(key)
    inputs = red.lrange("{}:inputs".format(key), 0, -1)
    outputs = red.lrange("{}:outputs".format(key), 0, -1)
    print("{} was called {} times:".format(key, int(method_count)))
    for ins, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key,
              ins.decode("utf-8"), out.decode("utf-8")))


class Cache:
    """
    Class to create a new Redis instance
    """
    def __init__(self):
        """
        Instantiates a new Redis instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores new data with a unique id into the Redis instance
        """
        val = str(uuid4())
        self._redis.set(val, data)
        return val

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float,
                                                                    none]:
        """
        Takes a key string argument and an optional
        Callable argument named fn that will be used
        to convert the data back to the desired format.
        """
        if not self._redis.get(key):
            return None

        value = self._redis.get(key)
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Returns the value associated with the given key as a string
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Returns the value associated with the given key as an integer
        """
        try:
            value = int(self._redis.get(key))
        except ValueError:
            value = 0
        return value
