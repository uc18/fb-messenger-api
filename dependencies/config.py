from functools import lru_cache

from config.config import Settings as Config



@lru_cache(maxsize=128)
def get_config() -> Config:
    return Config()