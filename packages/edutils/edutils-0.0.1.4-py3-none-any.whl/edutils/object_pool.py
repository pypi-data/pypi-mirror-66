"""
线程安全的实例池
    copy from https://github.com/btmorex/object_pool

Usage:
    1)
    import memcache
    import object_pool

    memcache_pool = ObjectPool(lambda: memcache.Client(['127.0.0.1:11211']), max_size=10)
    with memcache_pool.item() as memcache:
        memcache.set(b'key', b'value')

    2) without with
    try:
        memcache = memcache_pool.get()
    finally:
        memcache_pool.put(memcache)

    3) support timout argument
    try:
        memcache = memcache_pool.get(timeout=1.0)
    except ObjectPoolTimeout:
        import logging
        logging.warning('timed out trying to get memcache connection')
"""

__all__ = [
    'ObjectPoolTimeout',
    'ObjectPool'
]

import threading
from contextlib import contextmanager
from time import time


class ObjectPoolTimeout(RuntimeError):
    pass


class ObjectPool(object):

    def __init__(self, create, max_size=None):
        self._create = create
        self._max_size = max_size
        self._size = 0
        self._items = []
        self._mutex = threading.Lock()
        self._item_available = threading.Condition(self._mutex)

    def get(self, timeout=None):
        with self._mutex:
            if not self._items and (self._max_size is None or self._size < self._max_size):
                item = self._create()
                self._size += 1
            else:
                if timeout is not None:
                    end = time() + timeout
                while not self._items:
                    remaining = timeout
                    if timeout is not None:
                        remaining = end - time()
                        if remaining <= 0.0:
                            raise ObjectPoolTimeout
                    self._item_available.wait(remaining)
                item = self._items.pop()
        return item

    def put(self, item):
        with self._mutex:
            self._items.append(item)
            self._item_available.notify()

    @contextmanager
    def item(self):
        item = self.get()
        try:
            yield item
        finally:
            self.put(item)
