# encoding: utf-8
'''
Created on 31 мар. 2017 г.
Абстрактный монитор
@author: av.Kustov
'''
from abc import ABCMeta , abstractmethod

class AbstractProcessor(metaclass=ABCMeta):
    '''
    Абстрактный монитор
    '''
    config = None

    def __init__(self, config):
        self.config = config
     
    def start(self):
        self.execute()
            
    @abstractmethod
    def execute(self):
        return