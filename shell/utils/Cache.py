'''
Created on 5 апр. 2017 г.
Кэш
@author: av.Kustov 
'''

import hashlib
import pickle
import time
from abc import ABCMeta, abstractmethod

class Cache:
    """
    Кеш  декоратор.
        cache = Cache(a_cache_client)
    Аргументы:
    impl    Реализация кэша. должен содержать методы "set" и "get"
               
    Опции:
    enabled    Если `False`, игнорирется реализайия и всегда  отдаются реальные значения функции,
               даже если вызвать`.cached()`.
               Default: True
    bust       Если `True`, всегда переписываются данными реальной функции.
               Default: False
    """
    def __init__(self, impl= None, **default_options):
        self.impl = impl or SimpleCache()
        self.default_options = default_options

    def __call__(self, key = None, **kw):
        """
        возвращает декоратор
            @cache("mykey", ...)
            def exampl_method():
                # ...
            # или в  параметрах декоратора
            exampl_method = cache("mykey", ...)(exampl_method)
        Аргументы:
        key    (string)  -  ключ
        Опции:
        **kw
        """
        opts = self.default_options.copy()
        opts.update(kw)

        def _cache(fn):
            k = key or '<cache>/%s' % fn.__name__
            return CacheWrapper(self.impl, k, fn, **opts)

        return _cache
    
class CacheWrapper:
    """
    The result of using the cache decorator is an instance of
    CacheWrapper.
    Методы:
    get       (так же и __call__) Получение значения кэша,
              пересчет кэша если потребуется.
    cached    Получить значение кеша.  В случае когда значение не закеширована,
              врзвращается `default` величина . если значение отсутствует в кеше выкидывается исключение `KeyError`.
    refresh   потворное выполненние метода(оборачиваемого) и обновление значение кэша, согласно применяемой реализации кжша.
    """
    def __init__(self, impl, key, calculate,
                 bust=False, enabled=True, default='__absent__', **kw):
        self.impl = impl
        self.key = key
        self.calculate = calculate
        self.default = default

        self.bust = bust
        self.enabled = enabled

        self.options = kw

    def _has_default(self):
        return self.default != '__absent__'

    def _get_cached(self, *a, **kw):
        '''
        получить из кэша, значение
        '''
        if not self.enabled:
            return self.calculate(*a, **kw)

        key = _prepare_key(self.key, *a, **kw)
        cached = self.impl.get(key)

        if cached is None:
            raise KeyError

        return _unprepare_value(cached)

    def cached(self, *a, **kw):
        try:
            return self._get_cached(*a, **kw)
        except KeyError as e:
            if self._has_default():
                return self.default
            else:
                raise e

    def refresh(self, *a, **kw):
        '''
        обновить значение  в кэше
        '''
        fresh = self.calculate(*a, **kw)
        if self.enabled:
            key = _prepare_key(self.key, *a, **kw)
            value = _prepare_value(fresh)
            self.impl.set(key, value, **self.options)

        return fresh

    def get(self, *a, **kw):
        if self.bust:
            return self.refresh(*a, **kw)
        try:
            return self._get_cached(*a, **kw)
        except KeyError:
            return self.refresh(*a, **kw)

    def __call__(self, *a, **kw):
        return self.get(*a, **kw)

_CACHE_NONE = '_EMPTY_'


def _prepare_value(value):
    """
    подготовка значения
    """
    if value is None:
        return _CACHE_NONE
    return value

def _unprepare_value(prepared):
    if prepared == _CACHE_NONE:
        return None
    return prepared

def _prepare_key(key, *args, **kwargs):
    """
    подготовка хеша ключа
    """
    if not args and not kwargs:
        return key
    items = sorted(kwargs.items())
    hashable_args = (args, tuple(items))
    args_key = hashlib.md5(pickle.dumps(hashable_args)).hexdigest()
    return "%s/args:%s" % (key, args_key)


class AbstractCache:
    __metaclass__ = ABCMeta
    '''
     Шаблон для реализации кэша
    '''
    #содержимое кэша 
    _cache = {}
     
    @abstractmethod
    def set(self, key, val, **kw):
        pass
    
    @abstractmethod
    def get(self, key):
        pass
        
    
class SimpleCache(AbstractCache):
    '''
     Простой кеш
    '''
    def __init__(self):
        pass

    def set(self, key, val, **kw):
        self._cache[key] = val

    def get(self, key):
        return self._cache.get(key)


class ExpireCache(AbstractCache):
    '''
     Кеш с вытеснением по времени
    '''
    def __init__(self):
        self._expire = {}

    def set(self, key, val, **kw):
        self._cache[key] = val
        if kw.get('time', -1) == -1:
            self._expire[key] = -1
        else:
            self._expire[key] = time.time() + kw['time']

    def get(self, key):
        if key in self._cache:
            if self._expire[key] == -1 or self._expire[key] > time.time():
                return self._cache.get(key)
            else:
                del self._cache[key]
                del self._expire[key]
        return None


class ZerroCache(AbstractCache):
    '''
     Пустой кэш
    '''
    def set(self, key, val, **kw):
        pass

    def get(self, key):
        return None