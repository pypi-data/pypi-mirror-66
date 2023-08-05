import os
import time
import unittest

from cache_gs import CacheGS
from cache_gs.cache_classes.file_cache import FileCache
from cache_gs.utils.filesystem import remove_tree


class TestRealFileCache(unittest.TestCase):

    def setUp(self):
        self.cache_path = ".cache_dir"
        self.cache = CacheGS('path://'+self.cache_path)

    def tearDown(self):
        if os.path.isdir(self.cache_path):
            remove_tree(self.cache_path)

    def test_file_cache(self):
        self.assertIsInstance(self.cache, CacheGS)

    def test_get_set_delete(self):
        self.assertTrue(self.cache.set_value('sec', 'key', '1234'))
        self.assertEqual(self.cache.get_value('sec', 'key'), '1234')
        self.assertTrue(self.cache.delete_value('sec', 'key'))

    def test_purge(self):
        self.assertTrue(self.cache.set_value('sec', 'key', '1234', 0.1))
        time.sleep(0.2)
        self.assertGreater(self.cache.purge_expired(), 0)

    def test_exception_on_purge(self):
        self.cache.set_value(section=FileCache.CACHE_SECTION,
                             key=FileCache.LAST_PURGE,
                             value='error')

        cache = CacheGS('path://'+self.cache_path)
        self.assertIsInstance(cache, CacheGS)
