# encoding: utf-8
'''
Created on 30 мар. 2017 г.
Наблюдатель за COM объектом
@author: av.Kustov
'''
from shell.processors.AbstractProcessor import AbstractProcessor
from shell.processors.TimeoutError import *
from shell.utils.Observer import Publisher
from shell.event.MailProcessEvent import MailProcessEvent
from shell.event.SystemEvent import SystemEvent
from shell.event.KillProcessByComExpiredEvent import KillProcessByComExpiredEvent

import pythoncom
import win32com.client
from _overlapped import NULL
from mmsystem import MCI_FORMAT_MILLISECONDS
import logging

logger = logging.getLogger(__name__)

class ComObjectProcessor(AbstractProcessor):
    '''
    Наблюдатель за COM объектом
    '''
    #публикатор
    pub = None
    
    def __init__(self, config):
        self.config = config
        super(AbstractProcessor,self).__init__()
        #регим события обработки ошибки исполнения методо Com объекта
        self.pub = Publisher()
        self.pub.register(MailProcessEvent(self.config))
        self.pub.register(SystemEvent(self.config))
        self.pub.register(KillProcessByComExpiredEvent(self.config))
        
    def execute(self): 
        
        try:
            self.execute_com()
        except Exception as error:
            logger.error(error)
            #публикация события на обработчики
            self.pub.dispatch(error.__str__()) 
                      
    def execute_com(self): 

                live_timeout = int(self.config.witerezult)    
                @timeout(live_timeout) 
                def exec_com_method():
                    '''
                    исполнение методов - обертка
                    live_timeout - предельное время исполнениния метода
                    '''                    
                    logging.debug("Обработка Com методов")
                    #Сразу перед инициализацией DCOM в run() , для многопоточных приложений
                    pythoncom.CoInitializeEx(0)                   
      
                    ##win32com.client.GetActiveObject("meAppServer.AppServer")
                    #xl = win32com.client.dynamic.Dispatch("meAppServer.AppServer")
                
    #                 root = win32com.client.gencache.GetModuleForProgID("meAppServer.AppServer")                    
    #                 dispat = root.Dispatch('meAppServer.AppServer')
    #                 need = root.IAppServer2(dispat)
    #                 main = root.IAppServer(dispat)
                    
                    
                    #main =  win32com.client.Dispatch('meAppServer.AppServer')
                    #main = win32com.client.gencache.EnsureModule('{91A48AD8-D669-45BC-AD7C-C717E3BBEE23}', 0, 1, 2)
    
                    
                    main = win32com.client.dynamic.Dispatch("meAppServer.AppServer")
                    #ass = root.AppServer(main) 
                    #xl = win32com.client.DispatchEx("meAppServer.AppServer" )
                    #     addadd = win32com.client.gencache.GetModuleForCLSID('{91A48AD8-D669-45BC-AD7C-C717E3BBEE23}') 
                    #     addadd1 = win32com.client.gencache.GetModuleForProgID('IAppServer2') 
                    #     addadd.IAppServer2.ExecuteMethodAsXML("", "", "", "", "")
                    #xl._FlagAsMethod("SendTraceInfoMessage")
                    #x2 = win32com.client.gencache.EnsureDispatch(xl)
                    constants = win32com.client.constants 
                    #  print(xl.CLSID)
                  
                    errorinfo=NULL
                    SID = NULL
                    Value = ""
                    Props = ""
                    SesInfo=""
                    entityid = 6606
                    logging.debug("COM Авторизация")
                    
                    sss =  main.Authorize(self.config.com_login, self.config.com_password, "server", self.config.com_sysname, "", 0, errorinfo, SID)
                
                    SID = sss[2]
                    errorinfo = sss[1]
                    if errorinfo!='': raise Exception(errorinfo)
                    
                    SesInfoArr = main.GetCurrentSessionInfo(sss[2], SesInfo)
                    logging.debug('COM Информация по сессии %s' %  SesInfoArr.__str__())
                    
                    logging.debug("COM ВЫход пользователя")
                    log_out = main.LogOut(SID)
                    
                    # print(SesInfoArr)
                 
                    #  print(need.GetSysLibVersion())
                    #  print(need.GetCurrentSessionInfo(sss[2], SesInfo))
                    #rez = need.ExecuteMethodAsXML(sss[2],"<>","getUserInfo",[],[],)
                    # need.ExecuteStoredProc2(sss[2], "getUserInfo", "", "", "")
                    # xl.ExecuteStoredProc2(SID, "getUserInfo", "", "", "")
                    
                    #wmi = win32com.client.GetObject('winmgmts:')
                    #children = wmi.ExecQuery('Select * from win32_process ' )
                    
                    #handle = win32api.OpenProcess(1, 0, 1)
                    # win32api.TerminateProcess(handle, 0)
                    # win32api.CloseHandle(handle)
                    #x3 = main.SendTraceInfoMessage(1,1,1,1,1)
                    #print(x3)
     
                    pythoncom.CoInitializeEx(0)
                    
                exec_com_method()