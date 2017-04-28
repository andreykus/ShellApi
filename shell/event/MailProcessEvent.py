# encoding: utf-8
'''
Created on 31 мар. 2017 г.
Действие отсылки почты на событие
@author: av.Kustov
'''
from shell.event.AbstractEvent import AbstractEvent
from shell.processors.RealProces import RealProces

import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

class MailProcessEvent(AbstractEvent):
    '''
    Действие отсылки почты на событие
    '''
    proces = None
    #порядок обработки 
    order = 2
    #название события
    name = "MAil_Process"
    def __init__(self, config):
        self.config = config
        super(AbstractEvent,self).__init__()

    def sendMessage(self, message, title, sender, to, host = 'localhost', port = 25, user='test', password='test'):  
        '''
        Отослать сообщение
        message - сообщение
        title - тема письма
        sender - отправитель
        to - получатель
        host - почтовый сервер
        port - порт почтового сервера
        user - логин 
        '''  
        msg = MIMEText(message,'plain', 'utf-8')
        msg['Subject'] = 'Проблемы сиситемы %s (процесс не соответсвует метрикам, методы Com объекта исполняются с задержкой) %s' % (self.config.localhost, title)
        msg['From'] = sender
        msg['To'] = to
        
        smtp = smtplib.SMTP()

        smtp.connect(host, port)
        smtp.login(user, password)
        logger.debug('Send mail %s'% msg['To']) 
        smtp.sendmail(msg['From'] ,msg['To'], msg.as_string())
        smtp.quit()
     
    def sendMessages(self, message, title ): 
        '''
        Отослать сообщения
        message - сообщение
        title - тема письма
        ''' 
        for recipient in self.config.recipients:
            try:
                self.sendMessage(message ,title, self.config.sender, recipient, self.config.host, self.config.port, self.config.user, self.config.password)
            except Exception as error:
                logger.error(error)
    
    def exec(self, process): 
        '''
        Обработать сообщения
        process - сообщения
        ''' 
        logger.debug("Send mail")  
        #если это список процессов 
        if isinstance(process, list):         
            for proces in process:
                message = proces               
                if isinstance(proces, RealProces) and proces.is_running():
                        message = 'Внимание системное событие превышения метрик по процессу %s: загрузка CPU %s , загрузка памяти MEM %s ' %  (proces.__str__(),  proces.old_cpu_percent.__str__(), proces.old_memory_percent.__str__())             
                self.sendMessages(message.__str__(), "")
        else:        
            self.sendMessages(process.__str__(), "")