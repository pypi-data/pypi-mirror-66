import unittest
from time import time
from unittest.mock import Mock, patch

from cache_gs.cache_classes.redis_cache import RedisCache
from tests.test_tools import raise_test_exception


class TestRedisCache(unittest.TestCase):

    STRING_CONNECTION = 'redis://localhost:6379'

    @patch("redis.Redis", Mock())
    @patch("redis.Redis.from_url", Mock())
    def test_init(self):
        rc = RedisCache(self.STRING_CONNECTION)
        self.assertIsInstance(rc, RedisCache)
        self.assertEqual(rc.purge_expired(), 0)

    @patch("redis.Redis", Mock())
    @patch("redis.Redis.from_url", Mock())
    def test_get_set(self):
        rc = RedisCache(self.STRING_CONNECTION)
        rc.redis.get = lambda *args: b"abc"
        self.assertEqual(rc.get_value("sec", "key"), "abc")
        rc.redis.get = lambda *args: None
        self.assertIsNone(rc.get_value("sec", "key"))

        rc.redis.set = lambda *args, **kwargs: None
        self.assertTrue(rc.set_value("sec", "key", "abc"))
        self.assertTrue(rc.set_value("sec", "key", "abc", 10))
        self.assertTrue(rc.set_value("sec", "key", "abc", time()+10))

        rc.redis.delete = lambda *args, **kwargs: True
        self.assertTrue(rc.delete_value("sec", "key"))

    @patch("redis.Redis", Mock())
    @patch("redis.Redis.from_url", Mock())
    def test_get_set_exception(self):
        rc = RedisCache(self.STRING_CONNECTION)
        rc.redis.get = lambda *args: raise_test_exception('get')
        self.assertEqual(rc.get_value('sec', 'key', 'abc'), 'abc')
        rc.redis.set = lambda * args, **kwargs: raise_test_exception('set')
        self.assertFalse(rc.set_value('sec', 'key', 'abc'))
        rc.redis.delete = lambda *args, **kwargs: raise_test_exception(
            'delete')
        self.assertFalse(rc.delete_value("sec", "key"))
