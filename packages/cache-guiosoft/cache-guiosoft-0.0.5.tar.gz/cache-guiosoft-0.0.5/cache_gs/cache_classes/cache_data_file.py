import json
import os
import time

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.utils.logging import get_logger


class CacheDataFile:
    __slots__ = '_data', '_filename', 'log'

    def __init__(self, filename: str = None, cache_data: CacheData = None):
        self._data: CacheData = cache_data
        self._filename = filename
        self.log = get_logger()
        if filename and os.path.isfile(filename):
            self.load(filename)

    def load(self, filename) -> bool:
        success = False
        if os.path.isfile(filename):
            try:
                with open(filename, 'r', encoding='ascii') as f:
                    json_data = json.loads(f.read())

                section = json_data.get('section', None)
                key = json_data.get('key', None)
                value = json_data.get('value', None)
                ttl = json_data.get('ttl', 0)
                created = json_data.get('created', time.time())
                valid_until = 0 if ttl == 0 else created+ttl
                success = section and key and (
                    valid_until == 0 or valid_until >= time.time())

                if success:
                    self._data = CacheData(
                        section, key, value, ttl, created)
                    self._filename = filename
                else:
                    os.unlink(filename)

            except Exception as exc:
                self.log.error('EXCEPTION ON LOADING CACHE FILE: %s', str(exc))

        return success

    def save(self, filename) -> bool:
        success = False
        try:
            data = {
                "section": self._data.section,
                "key": self._data.key,
                "value": self._data.value,
                "ttl": self._data.ttl,
                "created": time.time() if self._data._created == 0 else self._data._created
            }
            with open(filename, 'w', encoding='ascii') as f:
                f.write(json.dumps(data, ensure_ascii=True, default=str))

            success = os.path.isfile(filename)
        except Exception as exc:
            self.log.error('EXCEPTION ON SAVING CACHE FILE: %s', str(exc))

        return success

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return "CacheDataFile('{filename}',{data})".format(
            filename=self._filename,
            data=self._data
        )
