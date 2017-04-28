# encoding: utf-8
'''
Created on 4 апр. 2017 г.
Логирование в системный монитор
@author: av.Kustov
'''
from shell.event.AbstractEvent import AbstractEvent
from shell.processors.RealProces import RealProces

import servicemanager
import logging

logger = logging.getLogger(__name__)

class SystemEvent(AbstractEvent):
    '''
    Логирование в системный монитор
    '''
    proces = None
    #порядок обработки 
    order = 3
    #название события
    name = "System event"
    def __init__(self, config):
        self.config = config
        super(AbstractEvent,self).__init__()

    def sendMessages(self, message):
        '''
        Сообщение стандартной сисиемы мониторига системы
        message - сообщение
        '''        
        servicemanager.LogErrorMsg("Системное событие  ошибки:  %s service" % (message))    
  
    def exec(self, process): 
        '''
        Обработать сообщения
        process - сообщения
        '''  
        logger.debug("Send system event")   
        #если это список процессов
        if isinstance(process, list):                    
            for proces in process:
                message = proces
                #если процесс активен, считать его метрики
                if isinstance(proces, RealProces) and proces.is_running():
                    message = 'Внимание системное событие превышения метрик по процессу %s: загрузка CPU %s , загрузка памяти MEM %s ' %  (proces.__str__(), proces.old_cpu_percent.__str__(), proces.old_memory_percent.__str__())                               
                self.sendMessages(message.__str__())
        else:        
            self.sendMessages(process.__str__())
    