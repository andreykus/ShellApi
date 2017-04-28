'''
Created on 7 апр. 2017 г.
Обертка для объекта процесс (Process)
@author: av.Kustov
'''
from psutil import Process

class RealProces(Process):
    '''
    Обертка для объекта процесс (Process)
    '''
    #значение загрузки памяти
    old_memory_percent = 0
    #значение загрузки процессора
    old_cpu_percent = 0

    def __init__(self, proces):
        self.old_cpu_percent = proces.cpu_percent()
        self.old_memory_percent = proces.memory_percent()
        super(Process, self).__init__()
        self._init(proces.pid)
    
        
        