"""`functools.lru_cache` compatible memoizing function decorators."""
__all__ = ('fifo_cache', 'lfu_cache', 'lru_cache', 'mru_cache', 'rr_cache', 'ttl_cache')
import math
import random
import time
try:
    from threading import RLock
except ImportError:
    from dummy_threading import RLock
from . import FIFOCache, LFUCache, LRUCache, MRUCache, RRCache, TTLCache
from . import cached
from . import keys

class _UnboundTTLCache(TTLCache):

    def __init__(self, ttl, timer):
        TTLCache.__init__(self, math.inf, ttl, timer)

def fifo_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a First In First Out (FIFO)
    algorithm.

    """
    def decorator(func):
        lock = RLock()
        key_func = keys.typedkey if typed else keys.hashkey
        wrapper = cached(cache=FIFOCache(maxsize), key=key_func, lock=lock)(func)
        wrapper.cache_parameters = lambda: {"maxsize": maxsize, "typed": typed}
        return wrapper
    return decorator

def lfu_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Frequently Used (LFU)
    algorithm.

    """
    def decorator(func):
        lock = RLock()
        key_func = keys.typedkey if typed else keys.hashkey
        wrapper = cached(cache=LFUCache(maxsize), key=key_func, lock=lock)(func)
        wrapper.cache_parameters = lambda: {"maxsize": maxsize, "typed": typed}
        return wrapper
    return decorator

def lru_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm.

    """
    def decorator(func):
        lock = RLock()
        key_func = keys.typedkey if typed else keys.hashkey
        wrapper = cached(cache=LRUCache(maxsize), key=key_func, lock=lock)(func)
        wrapper.cache_parameters = lambda: {"maxsize": maxsize, "typed": typed}
        return wrapper
    return decorator

def mru_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Most Recently Used (MRU)
    algorithm.
    """
    def decorator(func):
        lock = RLock()
        key_func = keys.typedkey if typed else keys.hashkey
        wrapper = cached(cache=MRUCache(maxsize), key=key_func, lock=lock)(func)
        wrapper.cache_parameters = lambda: {"maxsize": maxsize, "typed": typed}
        return wrapper
    return decorator

def rr_cache(maxsize=128, choice=random.choice, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Random Replacement (RR)
    algorithm.

    """
    def decorator(func):
        lock = RLock()
        key_func = keys.typedkey if typed else keys.hashkey
        wrapper = cached(cache=RRCache(maxsize, choice=choice), key=key_func, lock=lock)(func)
        wrapper.cache_parameters = lambda: {"maxsize": maxsize, "typed": typed}
        return wrapper
    return decorator

def ttl_cache(maxsize=128, ttl=600, timer=time.monotonic, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm with a per-item time-to-live (TTL) value.
    """
    def decorator(func):
        lock = RLock()
        key_func = keys.typedkey if typed else keys.hashkey
        if maxsize is None:
            cache = _UnboundTTLCache(ttl, timer)
        else:
            cache = TTLCache(maxsize, ttl, timer)
        wrapper = cached(cache=cache, key=key_func, lock=lock)(func)
        wrapper.cache_parameters = lambda: {"maxsize": maxsize, "ttl": ttl, "timer": timer, "typed": typed}
        return wrapper
    return decorator