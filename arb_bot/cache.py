import time

CACHE = {}

def get_cache(key):
    if key in CACHE:
        data, ts = CACHE[key]
        if time.time() - ts < 10:
            return data
    return None

def set_cache(key, value):
    CACHE[key] = (value, time.time())