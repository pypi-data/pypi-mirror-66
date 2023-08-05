import time
import unittest

from cache_gs.cache_classes.cache_data import CacheData


class TestCacheData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expired = CacheData('', 'expired', '0', 0.001)
        cls.valid = CacheData('', 'valid', 'value', 100)
        cls.eternal = CacheData('sec', 'eternal', 'value', 0)
        time.sleep(0.2)
        return super().setUpClass()

    def test_init(self):
        self.assertEqual(self.eternal.section, 'sec')
        self.assertEqual(self.eternal.key, 'eternal')
        self.assertEqual(self.eternal.value, 'value')
        self.assertEqual(self.eternal.ttl, 0)

    def test_valid(self):
        self.assertGreater(self.valid.valid_until, 0)
        self.assertFalse(self.valid.expired)

    def test_expired(self):
        self.assertTrue(self.expired.expired)

    def test_equal(self):
        cd1 = CacheData('sec', 'key', 'value', 0.1)
        cd2 = CacheData('sec', 'key', 'value', 0.1)
        self.assertTrue(cd1 == cd2)
        cd2 = CacheData('sec', 'key', 'value2', 0.1)
        self.assertFalse(cd1 == cd2)
        self.assertFalse(cd1 == 'another type')

    def test_repr(self):
        cd = CacheData('sec', 'key', 'value', 0)
        self.assertEqual(repr(cd), "CacheData('sec','key','value',0)")
        cd = CacheData('sec', 'key', 'value', 0, None)
        self.assertEqual(repr(cd), "CacheData('sec','key','value',0)")
