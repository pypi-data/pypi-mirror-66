import os
import unittest

from cache_gs import CacheGS
from cache_gs.cache_classes.file_cache import FileCache
from cache_gs.utils.filesystem import remove_tree


class TestFileCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_folder = '.cache'
        cls.file_cache = CacheGS('path://'+cls.cache_folder)
        cls.file_cache.set_value(
            'test', 'key', 'abcd', 0.001)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(cls.cache_folder):
            remove_tree(cls.cache_folder)
        return super().tearDownClass()

    def test_setup_error_folder(self):
        with self.assertRaises(Exception):
            FileCache('path://.cache_/error')

    def test_z_purge(self):
        self.assertGreater(self.file_cache.purge_expired(), 0)

    def test_get_default(self):
        self.assertEqual(self.file_cache.get_value(
            'test', 'key_', 'abcd'), 'abcd')
