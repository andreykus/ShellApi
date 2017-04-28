# encoding: utf-8
'''
Created on 29 мар. 2017 г.
Абстрактное действие на событие
@author: av.Kustov
'''
from abc import ABCMeta, abstractmethod
from shell.utils.Observer import  Subscriber

class AbstractEvent(Subscriber):
    __metaclass__ = ABCMeta
    '''
    Абстрактное действие на событие
    '''
    object_ = None
    order = 0
    
    def __init__(self, object_):
        self.object_ = object_
        super(Subscriber,self).__init__()    
     
    def update(self, process):
        self.exec(process)
        return
                              
    @abstractmethod
    def exec(self, process):
        '''
        метод реализуемый в наследнике
        '''
        return 