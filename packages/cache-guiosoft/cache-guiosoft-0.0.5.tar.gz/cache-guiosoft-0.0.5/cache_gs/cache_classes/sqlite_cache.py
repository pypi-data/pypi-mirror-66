import os
import sqlite3

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.interfaces.super_cache import SuperCache

DELETE_EXPIRED = """
DELETE FROM cache
WHERE valid_until BETWEEN 1 and strftime('%s','now');"""

CREATE_DB = """
PRAGMA auto_vacuum = 1;
PRAGMA journal_mode = WAL;
CREATE TABLE IF NOT EXISTS
    cache(section text, key text, value text, valid_until float);
CREATE UNIQUE INDEX IF NOT EXISTS idx_cache ON cache(section, key);
"""+DELETE_EXPIRED

SELECT_GET = """
SELECT value, valid_until
FROM cache
WHERE section =?
and key =?
and (valid_until=0 or valid_until > strftime('%s', 'now'))"""

INSERT = """
INSERT OR REPLACE INTO cache
(section,key,value,valid_until)
values (?,?,?,?)"""

DELETE = "DELETE FROM cache WHERE section=? and key=?"


class SQLiteCache(SuperCache):

    def setup(self):
        # expects a sqlite:path
        file_path = os.path.abspath(self._string_connection.split('://')[1])

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, 'cache.sqlite')

        try:
            self.log_debug('SQLite cache: %s', file_path)
            self.conn = sqlite3.connect(file_path)
            c = self.conn.cursor()
            c.executescript(CREATE_DB)
            self.conn.commit()
        except Exception as exc:
            self.log_error('ERROR ON CONNECT TO SQLITE CACHE: %s', str(exc))
            raise

    def _get_value(self, section: str, key: str, default=None) -> CacheData:
        result = None

        try:
            c = self.conn.cursor()
            f = c.execute(SELECT_GET, [section, key]).fetchone()
            if not f:
                f = [default, 0]
            result = CacheData(section, key, f[0], f[1])

        except Exception as exc:
            self.log_error('ERROR ON FETCH CACHE: %s', str(exc))

        return result

    def _set_value(self, data: CacheData) -> bool:
        success = False
        try:
            c = self.conn.cursor()
            exc = c.execute(INSERT,
                            [data.section,
                             data.key,
                             data.value,
                             data.valid_until])
            if c.rowcount > 0:
                self.conn.commit()
                success = True
            c.close()
        except Exception as exc:
            self.log_error('ERROR ON SET CACHE: %s', exc)

        return success

    def _delete_value(self, data: CacheData) -> bool:
        success = False
        try:
            c = self.conn.cursor()
            c.execute(DELETE,
                      [data.section, data.key])
            if c.rowcount > 0:
                self.conn.commit()
                success = True
            c.close()

        except Exception as exc:
            self.log_error('ERROR ON DELETE CACHE: %s', str(exc))

        return success

    def purge_expired(self) -> int:
        deleted = 0
        try:
            c = self.conn.cursor()
            c.execute(DELETE_EXPIRED)
            if c.rowcount > 0:
                self.conn.commit()
                deleted = c.rowcount
            else:
                self.conn.rollback()
            c.close()
        except Exception as exc:
            self.log_error('ERROR ON PURGE EXPIRED CACHE: %s', str(exc))

        return deleted
