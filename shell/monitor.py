# encoding: utf-8
'''
Created on 29 мар. 2017 г.
Мониторинг
@author: av.Kustov
'''
from shell.processors.ComObjectProcessor import ComObjectProcessor
from shell.processors.SystemJobProcessor import SystemJobProcessor
from shell.Config import *

import sys
import tkinter
import threading
from random import randint, choice
from tkinter import ttk
import sched, time

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

import pywintypes
import win32evtlogutil

from threading import Event, Thread

logger = logging.getLogger(__name__)
 
def call_repeatedly(interval, func, *args):
    '''
    исполнять функцию с интервалом
    interval -  интервал
    func - функция
    args - аргументы функции
    '''
    stopped = Event()
    def loop():
        while not stopped.wait(interval): 
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def print_time(a='default'):
    print("From print_time", time.time(), a)
    return True

def execAll(config):
    '''
    старт разделов мониторинга
    config - конфигурация сиситемы
    '''
    #процессы
    execSystem(config)
    #com объекты
    execCom(config)
    
def execSystem(config):
        '''
        мониторинг системного процесса
        config - конфигурация сиситемы
        '''    
        processor = SystemJobProcessor(config)
        processor.start()
        return
    
def execCom(config):
        '''
        мониторинг исполненния методов Com объекта
        config - конфигурация сиситемы
        '''
        processor = ComObjectProcessor(config)
        processor.start()
        return

class Shell(tkinter.Tk):   
    '''
    Основной класс старта мониторинга
    '''
    config = None  
             
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent 
        #конфигурация сиситемы
        self.config = ConfigManager(None)     
        self.initialize()   
    
    def show_event(self,event):
        print(event.x)

    def test_call_back(self): 
        def callback():
            percent=0
            count = 0
            while percent<100:
                time.sleep(0.1)
                logger.debug('test')
        t=threading.Thread(target=callback)
        t.start()
 
    def initialize(self):
        self.grid()  
           
        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        
        button = tkinter.Button(self,text=u"Старт",
                                command=self.OnButtonClick)
        
        button.grid(column=1,row=0)
        
        self.labelVariable = tkinter.StringVar()
        
        label = tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        
#         label = tkinter.Label(self,
#                               anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
    
        
    def startByShedule(self):
        '''
        старт задач по расписанию
        '''
        logger.debug( "Старт проверки событий")
        call_repeatedly(int(self.config.sys_delay), execAll, self.config)
        logger.debug( "Старт проверки серврерных событий")
        call_repeatedly(int(self.config.com_delay), execCom(self.config))
        
# #         self.labelVariable.set("You clicked the button !")
#         sysshed = sched.scheduler(time.time, time.sleep)
#         sysshed.enter(1, 1, call_repeatedly(60, print_time, "Hello, World"))
#         sysshed.run()
#        
#         comshed = sched.scheduler(time.time, time.sleep)
#         comshed.enter(3, 2, call_repeatedly(60, print_time, "Hello, World"))
#         comshed.run()
        
#         s.enter(5, 2, print_time, argument=('positional',))
#        s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
         
    def OnButtonClick(self):       
#         self.labelVariable.set("You clicked the button !")
        self.startByShedule()

    def OnPressEnter(self,event):
        logger.info ("You pressed enter !")   
        self.labelVariable.set("You clicked the button1 !")
       
def main(): 
    '''
    старт приложения
    '''  
    app = Shell(None)
    app.startByShedule()     
    #app.title('Монитор сосотояния ФОС')
    #app.mainloop()


class MonitorServiceSvc (win32serviceutil.ServiceFramework):
    '''
    Приложение как сервис
    '''
    _svc_name_ = "MonitorService"
    _svc_display_name_ = "MonitorService"
    _svc_description_ = "MonitorService"
 
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.hWaitResume = win32event.CreateEvent(None, 0, 0, None)
        self.timeout = 10000 #Пауза между выполнением основного цикла службы в миллисекундах
        self.resumeTimeout = 1000
        self._paused = False
 
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STOPPED,
#                               (self._svc_name_, ''))
       
    def SvcPause(self):
        self.ReportServiceStatus(win32service.SERVICE_PAUSE_PENDING)
        self._paused = True
        self.ReportServiceStatus(win32service.SERVICE_PAUSED)
        servicemanager.LogInfoMsg("The %s service has paused." % (self._svc_name_, ))
   
    def SvcContinue(self):
        self.ReportServiceStatus(win32service.SERVICE_CONTINUE_PENDING)
        win32event.SetEvent(self.hWaitResume)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg("The %s service has resumed." % (self._svc_name_, ))
               
 
    def SvcDoRun(self):
#         self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STARTED,
#                               (self._svc_name_,''))
        self.main()  
   
    #В этом методе реализовываем нашу службу    
    def main(self):
        self.app = Shell(None)
        #Здесь выполняем необходимые действия при старте службы
        servicemanager.LogInfoMsg("Hello! I'm a MonitorService.")
        while True:
            
            self.app.startByShedule()
            #Здесь должен находиться основной код сервиса
            servicemanager.LogInfoMsg("I'm still here.")
           
            #Проверяем не поступила ли команда завершения работы службы
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                #Здесь выполняем необходимые действия при остановке службы
                servicemanager.LogInfoMsg("Bye!")
                break
 
            #Здесь выполняем необходимые действия при приостановке службы
            if self._paused:
                servicemanager.LogInfoMsg("I'm paused... Keep waiting...")
            #Приостановка работы службы                
            while self._paused:
                #Проверям не поступила ли команда возобновления работы службы
                rc = win32event.WaitForSingleObject(self.hWaitResume, self.resumeTimeout)
                if rc == win32event.WAIT_OBJECT_0:
                    self._paused = False
                    #Здесь выполняем необходимые действия при возобновлении работы службы
                    servicemanager.LogInfoMsg("Yeah! Let's continue!")
                    break                  
 
 
         
if __name__ == '__main__':
 
#     if len(sys.argv) == 1:
#         servicemanager.Initialize()
#         servicemanager.PrepareToHostSingle(MonitorServiceSvc)
#         servicemanager.StartServiceCtrlDispatcher()
#     else:
#        win32serviceutil.HandleCommandLine(MonitorServiceSvc)
        
    main()