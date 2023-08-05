import os
import unittest
from time import sleep

from cache_gs import CacheGS
from cache_gs.utils.filesystem import remove_tree


class TestRealSQLiteCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_file = '.cache'
        if not os.path.isdir(cls.cache_file):
            os.mkdir(cls.cache_file)

        cls.cache = CacheGS('sqlite://' + cls.cache_file)
        cls.cache._cache.conn.set_trace_callback(print)
        cls.cache.set_value('sec', 'purged', '1234', 0.001)
        sleep(1)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        del (cls.cache)
        remove_tree(cls.cache_file)

    def test_init(self):
        self.assertIsInstance(self.cache, CacheGS)

    def test_get_set_delete(self):
        self.assertTrue(self.cache.set_value(
            'sec', 'key', '1234', ttl=100000))
        value = self.cache.get_value('sec', 'key')
        self.assertEqual(value, '1234')
        self.assertTrue(self.cache.delete_value('sec', 'key'))

    def test_z_purge(self):
        self.assertGreater(self.cache.purge_expired(), 0)
        self.assertEqual(self.cache.purge_expired(), 0)
