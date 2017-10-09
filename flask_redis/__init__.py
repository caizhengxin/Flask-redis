# -*- coding: utf-8 -*-
# @Author: caixin
# @Date:   2017-09-29 16:47:00
# @Last Modified by:   1249614072@qq.com
# @Last Modified time: 2017-10-09 17:03:45
"""
    flask.ext.redis
    ~~~~~~~~~~~~~~

    Adds captcha support to your application.

    :copyright: (c) 2017 by Thadeus Burgess.
    :license: BSD, see LICENSE for more details
"""
from __future__ import absolute_import
from __future__ import with_statement

__version__ = '0.1.0'

import redis
import msgpack
import logging

from functools import wraps
from flask import request, current_app

logger = logging.getLogger(__name__)


class Redis(object):
    """
    this class is used to control the redis objects.

    :param app: Flask instance, default `None`
    :param strict: Connection Type is `redis.StrictRedis` or `redis.Redis`,
                   defalut `StrictRedis`
    :param key_prefix: A prefix that should be added to all keys.

    """

    def __init__(self, app=None, strict=True,
                 key_prefix=None, *args, **kwargs):
        self._redis_class = redis.StrictRedis if strict else redis.Redis
        self._redis_kwargs = kwargs
        self.key_prefix = key_prefix or ''

        if app is not None:
            self.init_app(app)

    def init_app(self, app, *args, **kwargs):
        """init_app initialization"""
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        self._redis_kwargs.update(kwargs)
        self._redis_client = self._redis_class.from_url(
            redis_url, **self._redis_kwargs)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['redis'] = self

    def __getattr__(self, name):
        """Gets the property and returns the object."""
        return getattr(self._redis_client, name)

    def set_cache(self, key, value, timeout=None):
        """
        Set cache func.

        :param key: The `key` that needs to be cached.
        :param value: The `value` that needs to be cached.
        :param timeout: Default `None`. The `timeout` that needs to be cached.

        """
        dump = self.dump_object(value)
        return self._redis_client.set(self.key_prefix + key, dump, timeout)

    def mset_cache(self, data, timeout=None):
        """
        Mset cache func.

        :param data: The data is in the dictionary format.
        :param timeout: Default `None`. The `timeout` that needs to be cached.

        """
        pipe = self._redis_client.pipeline(transaction=False)

        for key, value in data.items():
            dump = self.dump_object(value)
            pipe.set(self.key_prefix + key, dump, timeout)
        pipe.execute()

    def get_cache(self, key):
        """
        Get cache func.

        :param key: The `key` that needs to be cached.

        """
        if not self.is_key(self.key_prefix + key):
            return
        return self.load_object(self._redis_client.get(self.key_prefix + key))

    def mget_cache(self, *keys):
        """
        Mget cache func.

        :param keys: The `keys` that needs to be cached.

        """
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]

        values = []
        for value in self._redis_client.mget(keys):
            if not value:
                values.append('')
            else:
                values.append(self.load_object(value))
        return values

    def delete(self, key):
        """
        delete cache func.

        :param key: The `key` that needs to be delete.

        """
        return self._redis_client.delete(self.key_prefix + key)

    def mdelete(self, *keys):
        """
        mdelete cache func.

        :param keys: The `keys` that needs to be delete.

        """
        if not keys:
            return
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        return self._redis_client.delete(*keys)

    def clear(self):
        """
        Clear cache func.

        """
        status = False
        if self.key_prefix:
            keys = self._redis_client.keys(self.key_prefix + '*')
            if keys:
                status = self._redis_client.delete(*keys)
        else:
            status = self._redis_client.flushdb()
        return status

    def cached(self, timeout=None, key_prefix='view/%s'):
        """
        Decorator. Use this to cache a function. By default the cache key
        is `view/request.path`. You are able to use this decorator with any
        function by changing the `key_prefix`. If the token `%s` is located
        within the `key_prefix` then it will replace that with `request.path`

        Example::

            # An example view function
            @redis.cached(timeout=5)
            def test_view():
                print(time.time())

            # An example misc function to cache.
            @redis.cached(key_prefix='key')
            def test_key():
                print(time.time())

        .. note::

            You MUST have a request context to actually called any
                functions that are cached.

        :param timeout: Default None. If set to an integer, will cache for that
                        amount of time. Unit of time is in seconds.

        :param key_prefix: Default `view/%(request.path)s`.

        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    cache_key = wrapper.make_cache_key(*args, **kwargs)
                    rcache = self.get_cache(cache_key)
                except Exception:
                    if current_app.debug:
                        raise
                    logger.exception(
                        "Exception possiblydue to cache backend.")
                    return func(*args, **kwargs)

                if not rcache:
                    rcache = func(*args, **kwargs)
                    try:
                        self.set_cache(
                            cache_key, rcache, timeout=wrapper.cache_timeout)
                    except Exception:
                        if current_app.debug:
                            raise
                        logger.exception(
                            "Exception possiblydue to cache backend.")
                        return func(*args, **kwargs)
                return rcache

            def make_cache_key(*args, **kwargs):
                if callable(key_prefix):
                    cache_key = key_prefix()
                elif '%s' in key_prefix:
                    cache_key = key_prefix % request.path
                else:
                    cache_key = key_prefix
                return cache_key

            wrapper.cache_timeout = timeout
            wrapper.make_cache_key = make_cache_key

            return wrapper
        return decorator

    def is_key(self, key):
        """
        Is_key func.

        :param key: The `key` that needs to be judged.

        """
        return self._redis_client.exists(key)

    def dump_object(self, value):
        """
        Dump_object func.

        :param value: The `value` that needs to be serialized.

        """
        return msgpack.dumps(value)

    def load_object(self, value):
        """
        Load_object func.

        :param value: The `value` that needs to be deserialized.

        """
        return msgpack.loads(value)
