from time import time

from cache_gs.utils.types import is_numeric, default_to


class CacheData:
    __slots__ = '_section', '_key', '_value', '_ttl', '_created'

    def __init__(self, section: str, key: str,
                 value: str, ttl: int, created: float = 0):
        section = default_to(section)
        key = default_to(key)
        if value is not None:
            value = str(value)

        self._section = section
        self._key = key
        self._value = value
        self._ttl = 0 if not is_numeric(ttl) or ttl < 0 else ttl
        self._created = created if is_numeric(
            created) and created > 0 else time()

    @property
    def section(self) -> str:
        return self._section

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> str:
        return self._value

    @property
    def ttl(self) -> int:
        """ Returns timestamp of expiration date (0 = never expires) """
        return self._ttl

    @property
    def valid_until(self) -> int:
        return self._created + self._ttl if self._ttl > 0 else 0

    @property
    def expired(self) -> bool:
        return time() > self.valid_until > 0

    def __eq__(self, value):
        if isinstance(value, self.__class__):
            return self.section == value.section and \
                self.key == value.key and \
                self.value == value.value and \
                self.ttl == value.ttl
        return False

    def __repr__(self):
        return "CacheData('{0}','{1}','{2}',{3}){4}".format(
            self.section,
            self.key,
            self.value,
            self.ttl,
            ' EXPIRED' if self.expired else ''
        )
