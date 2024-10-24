#!/usr/bin/env python3
''' Writing strings to Redis '''

import uuid
import redis
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    ''' count method calls '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' call method history '''
    @wraps(method)
    def wrapper(self, *args):
        input_key = f'{method.__qualname__}:inputs'
        self._redis.rpush(input_key, str(args))

        output_key = f'{method.__qualname__}:outputs'
        output = method(self, *args)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    '''  Retrieving lists '''
    input_key = '{}:inputs'.format(method.__qualname__)
    output_key = '{}:outputs'.format(method.__qualname__)

    input_vals = method.__self__._redis.lrange(input_key, 0, -1)
    output_vals = method.__self__._redis.lrange(output_key, 0, -1)

    print('{} was called {} times:'.format(
        method.__qualname__, len(input_vals)))

    for key, val in zip(output_vals, input_vals):
        print(
            '{}(*{}) -> {}'.format(
                method.__qualname__, val.decode("utf-8"), key.decode("utf-8")
            )
        )


class Cache:
    ''' cache class '''

    def __init__(self) -> None:
        ''' init the class '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' store data '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        ''' get value by its data type '''
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        ''' get value of key with the type of string '''
        value = self._redis.get(key)
        return str(value)

    def get_int(self, key: str) -> int:
        ''' get value of key with the type of integer '''
        value = self._redis.get(key)
        return int(value)
