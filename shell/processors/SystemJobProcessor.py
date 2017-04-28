# encoding: utf-8
'''
Created on 30 мар. 2017 г.
Наблюдатель за системным процессом
@author: av.Kustov
'''
from shell.processors.AbstractProcessor import AbstractProcessor
from shell.utils.Observer import Publisher
from shell.event.MailProcessEvent import MailProcessEvent
from shell.event.KillProcessEvent import KillProcessEvent
from shell.event.SystemEvent import SystemEvent
from shell.processors.RealProces import RealProces

import psutil
from psutil import NoSuchProcess
import logging

logger = logging.getLogger(__name__)

class SystemJobProcessor(AbstractProcessor):
    '''
    Наблюдатель за системным процессом
    '''
    #отобранные процессы
    bad_process = []
    #публикатор
    pub = None
    
    def __init__(self, config):
        self.config = config
        super(AbstractProcessor,self).__init__()
        #регистрируем подписчиков
        self.pub = Publisher()
        self.pub.register(KillProcessEvent(self.config))
        self.pub.register(SystemEvent(self.config))
        self.pub.register(MailProcessEvent(self.config))
        
    
    def findProcess(self, name):
        '''
        отобрать процессы по имени
        name - имя процесса
        '''
        list_process = []
        for proces in psutil.process_iter():
            if proces.name() == name:
                list_process.append(proces)
        return  list_process
           
    def chekprocess(self, proces):
        '''
        отобрать процессы не укладывающиеся в метрики с разницей maxcpuprocent , maxmemoryprocent
        proces - процесс
        '''          
        maxcpuprocent = int(self.config.maxcpuprocent)
        maxmemoryprocent = int(self.config.maxmemoryprocent)
        real = RealProces(proces)
              
        logger.debug('Проверка процесса %s CPU %s MEM %s'  % (proces.__str__(), real.old_cpu_percent.__str__(), real.old_memory_percent.__str__(),))
        if (real.old_cpu_percent>maxcpuprocent) or (real.old_memory_percent>maxmemoryprocent):
            message = 'Внимание системное событие превышения метрик по процессу %s: загрузка CPU %s , загрузка памяти MEM %s ' %  (proces.__str__(), real.old_cpu_percent.__str__(), real.old_memory_percent.__str__())
            logger.error(message)
            self.bad_process.append(real)
                     
        #proces.username()
        #proces.memory_full_info()
        
    def execute(self):     
        logger.debug("Обработка системных событий")
        self.bad_process = []
        try:
            #str1=" ".join(str(x) for x in plist)
            process = self.findProcess(self.config.process_name)
            if len(process) == 0 : raise NoSuchProcess(0, self.config.process_name ,'Не найден процесс %s' %  self.config.process_name) 
            for proces in process:              
                self.chekprocess(proces)  
                        
            if len(self.bad_process) !=0 :
                #публикация события на обработчики
                self.pub.dispatch(self.bad_process)
                                                                        
        except Exception as error:
            logger.error(error.__str__()) 