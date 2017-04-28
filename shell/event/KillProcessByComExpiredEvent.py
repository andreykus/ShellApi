# encoding: utf-8
'''
Created on 6 апр. 2017 г.
Действие выгрузки процесса на событие - выгружается самый загруженный процесс , из кеша сформированного исполнителем Com объектов
@author: av.Kustov
'''
from shell.event.AbstractEvent import AbstractEvent
from shell.utils.Cache import _prepare_key
from shell.processors.RealProces import RealProces

import psutil
import signal
from psutil import NoSuchProcess
import logging

logger = logging.getLogger(__name__)

NoneZerro = lambda par: 1 if par==0 else par

class KillProcessByComExpiredEvent(AbstractEvent):
    '''
    Действие выгрузки процесса на событие - выгружается самый загруженный процесс , из кеша сформированного исполнителем Com объектов
    '''
    
    proces = None
    #название события
    name = "Kill_Process_COM"
    #порядок обработки
    order = 110    
    
    def __init__(self, config):
        self.config = config
        super(AbstractEvent,self).__init__()
    
    def sortByBuzyTime(self, process):
        return 1
    
    def findProcess(self, name):
        '''
        отобрать процессы по имени
        name - имя процесса
        '''
        list_proces = []
        for proces in psutil.process_iter():
            if proces.name() == name:
                list_proces.append(RealProces(proces))
        return  list_proces
    
    def isWarnProces(self, proces):   
        '''
        выделить процесс с расхождением действительной метрики от минимальной за время на  alarm_metric процентов
        proces - процесс
        '''
        alarm_metric = int(self.config.com_alarm_metric)
        time_cache = int(self.config.com_time_cache)
        cache = self.config.cacheProcess  
                           
        @cache("pid", time = time_cache)    
        def getProcess(pid = None):         
            return proces 
        
        def upadateCache(pid = None):
            '''
            обновить кэш если новые метрики меньше текущих
            pid - идентификатор процесса            
            '''
            retProces = getProcess(proces.pid)
            
            key_ = _prepare_key("pid", pid)
            proces_cache = cache.impl.get(key_)
            
            if (proces_cache!=None) :            
                logger.debug('Память процесса %s реал %s , кэш %s ' % ( proces.pid , proces.old_memory_percent.__str__(), proces_cache.old_memory_percent.__str__()))
                logger.debug('CPU процесса %s реал %s , кэш %s ' % ( proces.pid,  proces.old_cpu_percent.__str__() , proces_cache.old_cpu_percent.__str__()))
            
            if (proces_cache!=None) and (proces.old_memory_percent < proces_cache.old_memory_percent) and (proces.old_cpu_percent < proces_cache.old_cpu_percent):
                del cache.impl._cache[key_]
                del cache.impl._expire[key_]  
                retProces = getProcess(proces.pid)            
        
            return retProces
        
        procesOld = upadateCache(proces.pid) 
              
        if ((proces.old_memory_percent/NoneZerro(procesOld.old_memory_percent))  > alarm_metric) or ((proces.old_cpu_percent/NoneZerro(procesOld.old_cpu_percent))  > alarm_metric):
            return True
                
        return False
              
    def getWarnProcess(self):
        '''
        процессы для выгрузки
        '''
        self.dif_process = []                                    
        process = self.findProcess(self.config.process_name)
        if len(process) == 0 : raise NoSuchProcess(0, self.config.process_name ,'Не найден процесс %s' %  self.config.process_name) 
        for proces in process:                                    
            if self.isWarnProces(proces):       
                self.dif_process.append(proces)                     
        return  self.dif_process     
            
    def killProcess(self, process):
        '''
        убить процесс
        process - процессы
        '''
        for proces in process:
            try: 
                if proces.is_running(): 
                    logger.debug('Kill process %s' % proces.__str__())     
                    proces.send_signal(signal.SIGTERM)        
            except Exception as error:
                logger.error(error.__str__())
        
    def exec(self, process):
        '''
        Обработать сообщения
        process - сообщения
        '''   
        logger.debug("Kill process COM Cache")                   
        warns = self.getWarnProcess()        
        self.killProcess(warns)       
        
    def removeNotActive(self, cache):
            process = cache.impl._cache
            if process!=None and len(process)>0:
                for proces in process :
                    if not proces.is_running():
                        key = _prepare_key("pid", proces.pid())
                        del process[key]
                        del cache.impl._expire[key]
            pid = 0 
            proces_new = proces
            key = _prepare_key("pid", pid)
            proces_old = cache.impl.get(key)
            if proces_old!= None and proces!= None:
                if proces_old.is_running() and proces.is_running():
                    if proces.cpu_percent()<proces_old.cpu_percent() or proces.memory_percent()<proces_old.memory_percent():
                        proces_new = proces_old
                        cache.impl._expire[key]=0
            print(proces_new)              
            #         cache = self.config.cacheProcess 
#         if cache!= None:
#             process = cache.impl._cache
#             self.removeNotActive(cache) 
#             if process!=None and len(process)>0:
#                               
#                 newProcess = sorted(process, key = self.sortByBuzyTime)                      
        