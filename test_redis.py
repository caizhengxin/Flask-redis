# -*- coding: utf-8 -*-
# @Author: caixin
# @Date:   2017-09-30 11:16:28
# @Last Modified by:   1249614072@qq.com
# @Last Modified time: 2017-10-09 17:20:51
from __future__ import with_statement
from __future__ import print_function

import sys
import time

from flask import Flask
from flask.ext.redis import Redis


if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class RedisTestCase(unittest.TestCase):

    def _set_app_config(self, app):
        app.config['REDIS_URL'] = 'redis://localhost:6379/0'

    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        self._set_app_config(app)
        self.redis = Redis(app)
        self.app = app

    def tearDown(self):
        self.app = None
        self.redis = None
        self.tc = None

    def test_setcache(self):
        self.redis.set_cache('setcache', {"test": "python"}, 200)

    def test_getcache(self):
        data = self.redis.get_cache('setcache')
        print(data)
        assert data == {b"test": b"python"}

    def test_lpush(self):
        print(self.redis.lpush('lpush', 'lpush'))

    def test_msetcache(self):
        self.redis.mset_cache({'a': 1, 'b': 2})

    def test_mgetcache(self):
        assert self.redis.mget_cache('a', 'b') == [1, 2]

    def test_mdelete(self):
        self.redis.mset_cache({'c': 1, 'd': 2})
        self.redis.mdelete('c', 'd')

        assert self.redis.is_key('c') == 0

    # def test_clear(self):
        # self.redis.clear()

    def test_cached(self):

        @self.app.route('/')
        @self.redis.cached(timeout=5)
        def cached_view():
            return str(time.time())

        tc = self.app.test_client()

        rv = tc.get('/')
        print(rv.data)
        the_time = rv.data
        time.sleep(2)
        rv = tc.get('/')
        assert the_time == rv.data
        time.sleep(5)
        rv = tc.get('/')
        assert the_time != rv.data


if __name__ == '__main__':
    unittest.main()
