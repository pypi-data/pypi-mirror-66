from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.utils.logging import get_logger


class SuperCache:

    def __init__(self, string_connection: str, **extra_args):
        if not isinstance(string_connection, str) or not string_connection:
            raise AttributeError(
                "bad string connection for {0}".format(type(self.__class__)))
        self._string_connection = string_connection
        self._extra_args = extra_args
        self.setup()

    def setup(self):
        raise NotImplementedError

    def _get_value(self, section: str, key: str, default=None) -> CacheData:
        raise NotImplementedError

    def _set_value(self, data: CacheData) -> bool:
        raise NotImplementedError

    def _delete_value(self, data: CacheData) -> bool:
        raise NotImplementedError

    def get_value(self, section: str, key: str, default=None) -> str:
        data = self._get_value(section, key, default)
        if not data or data.expired:
            return default

        return data.value

    def set_value(self, section: str, key: str,
                  value: str, ttl: int = 0) -> bool:
        data = CacheData(section, key, value, ttl)
        return self._set_value(data)

    def delete_value(self, section: str, key: str) -> bool:
        data = CacheData(section, key, None, 0)
        return self._delete_value(data)

    def purge_expired(self) -> int:
        raise NotImplementedError

    @classmethod
    def log_debug(cls, text, *args, **kwargs):
        get_logger().debug(text, *args, **kwargs)

    @classmethod
    def log_info(cls, text, *args, **kwargs):
        get_logger().info(text, *args, **kwargs)

    @classmethod
    def log_error(cls, text, *args, **kwargs):
        get_logger().error(text, *args, **kwargs)


class CacheException(Exception):
    pass
