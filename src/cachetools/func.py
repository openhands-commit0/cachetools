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
    lock = RLock()
    key_func = keys.typedkey if typed else keys.hashkey
    return cached(cache=FIFOCache(maxsize), key=key_func, lock=lock)

def lfu_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Frequently Used (LFU)
    algorithm.

    """
    lock = RLock()
    key_func = keys.typedkey if typed else keys.hashkey
    return cached(cache=LFUCache(maxsize), key=key_func, lock=lock)

def lru_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm.

    """
    lock = RLock()
    key_func = keys.typedkey if typed else keys.hashkey
    return cached(cache=LRUCache(maxsize), key=key_func, lock=lock)

def mru_cache(maxsize=128, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Most Recently Used (MRU)
    algorithm.
    """
    lock = RLock()
    key_func = keys.typedkey if typed else keys.hashkey
    return cached(cache=MRUCache(maxsize), key=key_func, lock=lock)

def rr_cache(maxsize=128, choice=random.choice, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Random Replacement (RR)
    algorithm.

    """
    pass

def ttl_cache(maxsize=128, ttl=600, timer=time.monotonic, typed=False):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm with a per-item time-to-live (TTL) value.
    """
    pass