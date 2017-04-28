'''
Created on 30 мар. 2017 г.

@author: bush
'''
import win32com
import win32com.client
import win32api
from _overlapped import NULL
from mmsystem import MCI_FORMAT_MILLISECONDS


print("ddddddddddddd")
if (1==1):
# try:
    ##win32com.client.GetActiveObject("meAppServer.AppServer")
    xl = win32com.client.dynamic.Dispatch("meAppServer.AppServer")
    
    root = win32com.client.gencache.GetModuleForProgID("meAppServer.AppServer")    
    dispat = root.Dispatch('meAppServer.AppServer')
    win32com.client.gencache.EnsureModule('{91A48AD8-D669-45BC-AD7C-C717E3BBEE23}', 0, 1, 2)
    need = root.IAppServer2(dispat)
    main = root.IAppServer(dispat)
    #ass = root.AppServer(main) 
#     xl = win32com.client.DispatchEx("meAppServer.AppServer" )
#     addadd = win32com.client.gencache.GetModuleForCLSID('{91A48AD8-D669-45BC-AD7C-C717E3BBEE23}') 
#     addadd1 = win32com.client.gencache.GetModuleForProgID('IAppServer2') 
#     addadd.IAppServer2.ExecuteMethodAsXML("", "", "", "", "")
    #xl._FlagAsMethod("SendTraceInfoMessage")
    #x2 = win32com.client.EnsureDispatch(xl)
    constants = win32com.client.constants 
  #  print(xl.CLSID)
  
    errorinfo=NULL
    SID = NULL
    Value = ""
    Props = ""
    SesInfo=""
    entityid = 6606
    sss =  main.Authorize("master", "", "server", "ФронтОфис", "", 0, errorinfo, SID)

    SID = sss[2]
    SesInfoArr = main.GetCurrentSessionInfo(sss[2], SesInfo)
    print(SesInfoArr)
 
    print(need.GetSysLibVersion())
    print(need.GetCurrentSessionInfo(sss[2], SesInfo))
    rez = need.ExecuteMethodAsXML(sss[2],"<>","getUserInfo",[],[],)
   # need.ExecuteStoredProc2(sss[2], "getUserInfo", "", "", "")
   # xl.ExecuteStoredProc2(SID, "getUserInfo", "", "", "")
    
    wmi = win32com.client.GetObject('winmgmts:')
    children = wmi.ExecQuery('Select * from win32_process ' )
    
    #handle = win32api.OpenProcess(1, 0, 1)
    # win32api.TerminateProcess(handle, 0)
    # win32api.CloseHandle(handle)
    x3 = main.SendTraceInfoMessage(1,1,1,1,1)
    print(x3)
    print("ddddddddddddd")
# except Exception as error:
#     print (error)
#     print (vars(error))
#     print (error.args)


if __name__ == '__main__':
    pass