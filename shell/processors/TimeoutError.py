# encoding: utf-8
'''
Created on 31 мар. 2017 г.
Генератор исключения времени исполненния
@author: av.Kustov
'''

from threading import Thread
import functools

class TimeoutError(Exception):
    '''
    Исключение при превышении времени исполненния
    '''
    pass
 
def timeout(timeout):
    '''
    описание декоратора на методе
    timeout - время жизни исполненния метода
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [TimeoutError('Время выполенения функции [%s] превысило допустимые [%s seconds] !' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return decorator