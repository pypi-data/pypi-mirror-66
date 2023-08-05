from redis import Redis

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.interfaces.super_cache import SuperCache


class RedisCache(SuperCache):
    """
    Connection string
    redis://localhost:6379?ConnectTimeout=5000&IdleTimeOutSecs=180
    """

    def setup(self):
        self.redis: Redis = Redis.from_url(self._string_connection)
        self.redis.memory_purge()

    def _get_value(self, section: str, key: str, default=None) -> CacheData:
        try:
            value = self.redis.get(self.section_key(section, key))
        except Exception as exc:
            self.log_error('GSCache REDIS GET ERROR: %s', exc)
            value = None
        if value:
            return CacheData(section, key, value.decode('utf-8'), 0)
        return CacheData(section, key, default, 0)

    def _set_value(self, data: CacheData) -> bool:
        try:
            self.redis.set(
                key=self.section_key(data.section, data.key),
                value=data.value,
                ex=data.ttl if data.ttl > 0 else None)
            return True

        except Exception as exc:
            self.log_error('GSCache REDIS SET ERROR: %s', exc)

        return False

    def _delete_value(self, data: CacheData) -> bool:
        try:
            self.redis.delete(self.section_key(data.section, data.key))
            return True
        except Exception as exc:
            self.log_error('GSCache REDIS DELETE ERROR: %s', exc)
        return False

    def purge_expired(self) -> int:
        return 0

    @staticmethod
    def section_key(section, key) -> str:
        return ('_' if not section else str(section))+':' +\
            ('_' if not key else str(key))
