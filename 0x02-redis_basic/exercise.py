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
    def wrapper(self, *args, **kwargs):
        """Helper function"""
        key = method.__qualname__
        if self._redis.get(key) is None:
            self._redis.set(key, 0)
        self._redis.incr(key)
        return method(self, *args, **kwargss)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history
    for a particular function in Redis
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Helper function"""
        key = method.__qualname__
        self._redis.rpush(f'{key}:inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f'{key}:outputs', str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Prints the call history of the method passed as a parameter
    """
    redis_instance = method.__self__._redis
    key = method.__qualname__
    n_calls = redis_instance.get(key).decode("utf-8")
    print(f'{key} was called {n_calls} times:')
    f_inputs = redis_instance.lrange(f'{key}:inputs', 0, -1)
    f_outputs = redis_instance.lrange(f'{key}:outputs', 0, -1)
    f_inout = list(zip(f_inputs, f_outputs))
    for input, output in f_inout:
        input = input.decode('utf-8')
        output = output.decode('utf-8')
        print(f"{key}(*{input}) -> {output}")


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
        id = str(uuid4())
        self.redis.set(id, data)
        return id

    def get(self, key: str, fn: Callable = None):
        """
        Takes a key string argument and an optional
        Callable argument named fn that will be used
        to convert the data back to the desired format.
        """
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
