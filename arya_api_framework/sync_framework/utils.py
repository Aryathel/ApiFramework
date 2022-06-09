from typing import Union
from functools import wraps
import time
import logging
from pathlib import Path

try:
    from ratelimit import RateLimitException
except ImportError:
    pass

_log = logging.getLogger('arya_api_framework.Sync')


def chunk_file_reader(file: Union[str, Path]):
    with open(file, 'rb') as f:
        chunk = f.read(64 * 1024)

        while chunk:
            yield chunk
            chunk = f.read(64 * 1024)


def sleep_and_retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RateLimitException as exception:
                _log.info(f"Applying rate limit: Sleeping for {exception.period_remaining}s")
                time.sleep(exception.period_remaining)
    return wrapper
