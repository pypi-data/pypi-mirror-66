from functools import wraps
from typing import Any, Callable, Optional

from ..backends.interface import Backend
from ..key import get_cache_key, get_cache_key_template, register_template
from ..typing import FuncArgsType
from .defaults import CacheDetect, _default_store_condition, context_cache_detect

__all__ = ("cache",)


def cache(
    backend: Backend,
    ttl: int,
    func_args: FuncArgsType = None,
    key: Optional[str] = None,
    store: Optional[Callable[[Any], bool]] = None,
    prefix: str = "",
):
    """
    Simple cache strategy - trying to return cached result,
    execute wrapped call and store a result with ttl if condition return true
    :param backend: cache backend
    :param ttl: duration in seconds to store a result
    :param func_args: arguments that will be used in key
    :param key: custom cache key, may contain alias to args or kwargs passed to a call
    :param store: callable object that determines whether the result will be saved or not
    :param prefix: custom prefix for key
    """
    store = _default_store_condition if store is None else store

    def _decor(func):
        _key_template = key
        if key is None:
            _key_template = f"{prefix}:{get_cache_key_template(func, func_args=func_args, key=key)}:{ttl}"
        register_template(func, _key_template)

        @wraps(func)
        async def _wrap(*args, _from_cache: CacheDetect = context_cache_detect, **kwargs):
            _cache_key = get_cache_key(func, _key_template, args, kwargs, func_args)
            cached = await backend.get(_cache_key)
            if cached is not None:
                _from_cache.set(_cache_key, ttl=ttl)
                return cached
            result = await func(*args, **kwargs)
            if store(result, args, kwargs):
                await backend.set(_cache_key, result, expire=ttl)
            return result

        return _wrap

    return _decor
