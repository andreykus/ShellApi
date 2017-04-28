# encoding: utf-8
'''
Created on 31 мар. 2017 г.
Наблюдатель
@author: av.Kustov
'''

from abc import ABCMeta, abstractmethod

import logging

logger = logging.getLogger(__name__)

class Subscriber(metaclass=ABCMeta):
    '''
    Подписчика на событие
    '''

    @abstractmethod    
    def update(self, message):
        logger.info('{} событие "{}"'.format(self.name, message))
        
        
class Publisher:
    '''
    Издатель события
    '''
    
    def __init__(self):
        # maps event names to subscribers
        # str -> dict
        self.events = {  }
        
    def get_subscribers(self, eventname):
        return self.events[eventname]
    
    def register(self, event , callback = None):
        self.events[event.name] = event         
        callback = getattr(event, 'update')
        order = getattr(event, 'order')
        self.events[event.name] = {'action':callback,'order':order }
        
    def unregister(self, eventname):
        del self.events[eventname]
    
    def sortByOrder(self, inputelement):
        return self.events[inputelement].get('order')
        
    def dispatch(self, message):
        newList = sorted(self.events, key = self.sortByOrder)
        for eventname in newList:           
            try:
                self.events[eventname].get('action')(message)                
            except Exception as error:
                logger.error(error)