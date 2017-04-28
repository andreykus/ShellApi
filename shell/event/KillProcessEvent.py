# encoding: utf-8
'''
Created on 31 мар. 2017 г.
Действие выгрузки процесса на событие
@author: av.Kustov
'''
from shell.event.AbstractEvent import AbstractEvent

import signal
import logging

logger = logging.getLogger(__name__)

class KillProcessEvent(AbstractEvent):
    '''
    Действие выгрузки процесса на событие
    '''
    proces = None
    #название события
    name = "Kill_Process"
    #порядок обработки 
    order = 100
    def __init__(self, config):
        self.config = config
        super(AbstractEvent,self).__init__()

    def exec(self, process):  
        '''
        Обработать сообщения
        process - сообщения
        ''' 
        logger.debug("Kill process")                  
        for proces in process:
            try:
                if proces.is_running():   
                    logger.debug('Kill process %s' % proces.__str__())     
                    proces.send_signal(signal.SIGTERM)        
                    #proces.kill()
            except Exception as error:
                logger.error(error.__str__())
        