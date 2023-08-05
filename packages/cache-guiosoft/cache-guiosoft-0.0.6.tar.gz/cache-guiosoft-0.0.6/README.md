# CACHE GUIOSOFT

Caching data using files, Redis or local SQLite


[![codecov](https://codecov.io/gh/guionardo/py-cache-guiosoft/branch/develop/graph/badge.svg)](https://codecov.io/gh/guionardo/py-cache-guiosoft)
![Codecov push](https://github.com/guionardo/py-cache-guiosoft/workflows/Codecov%20push/badge.svg)



[![codecov](https://codecov.io/gh/guionardo/py-cache-guiosoft/branch/develop/graphs/commits.svg)]

![Upload Python Package](https://github.com/guionardo/py-cache-guiosoft/workflows/Upload%20Python%20Package/badge.svg)

## Local files for caching

``` python
from cache_gs import CacheGS

# Storage on local directory

file_cache = CacheGS('path://directory_for_cache_storage')

# Storage on local SQLite database

slite_cache = CacheGS('sqlite://directory_or_file_for_storage')

# Storage on Redis

redis_cache = CacheGS('redis://host:6379')

[More options for redis](#Redis options and example)

```

## Usage

Like INI files, data is grouped in section/key names.

### Installing

``` bash
pip install cache-guiosoft
```

### Writing value

``` python
cache.set_value(section, key, value, ttl: int = 0)

# ttl is the life time of value in seconds from the time is created
```

### Reading value

``` python
value = cache.get_value(section, key, default=None)
```

### Deleting value

``` python
cache.delete_value(section, key)
```

### Purging expired data

* On *Redis* cache, this is handled by the server, automatically.
* On *SQLite* cache, purging is executing on every instantiation.
* On *Local File* cache, purging is automatically executed once a day, checked on every instantiation.

### Force purging expired data

``` python
cache.purge_expired()
```

### Redis options and example

Redis connection uses the [redis-py component](https://github.com/andymccurdy/redis-py) from Andy McCurdy.
You can use the same connection strings that the Redis class uses:

* redis://[[username]:[password]]@localhost:6379/0
* rediss://[[username]:[password]]@localhost:6379/0
* unix://[[username]:[password]]@/path/to/socket.sock?db=0

        Three URL schemes are supported:

        - ```redis://``
          <http://www.iana.org/assignments/uri-schemes/prov/redis>`_ creates a
          normal TCP socket connection
        - ```rediss://``
          <http://www.iana.org/assignments/uri-schemes/prov/rediss>`_ creates a
          SSL wrapped TCP socket connection
        - ``unix://`` creates a Unix Domain Socket connection

        There are several ways to specify a database number. The parse function
        will return the first specified option:
            1. A ``db`` querystring option, e.g. redis://localhost?db=0
            2. If using the redis:// scheme, the path argument of the url, e.g.
               redis://localhost/0
            3. The ``db`` argument to this function.

        If none of these options are specified, db=0 is used.

### Redis on docker

docker-compose.yaml

``` yaml
redis:
    container_name: 'redis'
    image: 'redis:4-alpine'
    command: redis-server --requirepass 1234
    ports:
        - '6379:6379'
```

For testing, just run:

``` bash
docker-compose up
```
