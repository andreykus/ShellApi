# encoding: utf-8
'''
Created on 29 мар. 2017 г.
Конфигурация
@author: av.Kustov
'''

from shell.utils.Cache import (Cache, ExpireCache)

import configparser
import logging
import socket

logger = logging.getLogger(__name__)

class ConfigManager(object):
    '''
    Класс начитки конфигурации монитора
    '''
    # повторять проверку сосотояния процесса каждые ? секунд
    sys_delay = 1 
    # повторять проверку сосотояния методов COM объекта каждые ? секунд
    com_delay = 1
    # логин FA#
    com_login = "master"
    # пароль FA#
    com_password = ""
    # подсиситема FA#
    com_sysname = ""
    # название системного процесса
    process_name = ""
    # максимальная загрузка процессора на процессе
    maxcpuprocent = 0
    # максимальное использование памяти на процессе
    maxmemoryprocent = 0
    # конфиг
    config = None
    #	получатели сообщений
    recipients = []
    # хост почтового сервера
    host = "127.0.0.1"
    # порт почтового сервера
    port = 25
    # логин почтового сервера
    user = "test"
    # пароль почтового сервера
    password = "test"
    # ожидать ответа от COM объекта
    witerezult = 10
    # имя локального хоста
    localhost = ""
    # кэш с вытеснением по времени    
    cacheProcess = Cache(ExpireCache())
    
    def loadcfg(self):
        '''
        загрузить конфигурацию
        '''    
        self.config = configparser.RawConfigParser()
        self.config.read("config.cfg","utf8")
        
        self.sys_delay = self.config.get("shellprocess", "delay")
        self.process_name = self.config.get("shellprocess", "name")
        self.maxcpuprocent = self.config.get("shellprocess", "maxcpuprocent")
        self.maxmemoryprocent = self.config.get("shellprocess", "maxmemoryprocent") 
                       
        self.com_delay = self.config.get("commethod", "delay")
        self.witerezult = self.config.get("commethod", "witerezult")
        self.com_login = self.config.get("commethod", "login")
        self.com_password = self.config.get("commethod", "password")
        self.com_sysname = self.config.get("commethod", "sysname")
        self.com_time_cache = self.config.get("commethod","time_cache")
        self.com_alarm_metric = self.config.get("commethod","alarm_metric")
            
        self.recipients = self.config.get("mail", "recipients").split(",")
        self.sender = self.config.get("mail", "sender")
        self.host = self.config.get("mail", "host")
        self.port = self.config.get("mail", "port")
        self.user = self.config.get("mail", "user")
        self.password = self.config.get("mail", "password")

        self.localhost = socket.gethostname()
        
    def printContain(self):
        '''
        распечатать конфигурвцию
        '''
        for section in self.config.sections():
            logger.debug("Секция: %s" % section)
            for options in self.config.options(section):
                logging.debug("x %s:::%s:::%s" % (options,
                                          self.config.get(section, options),
                                          str(type(options))))

    def __init__(self, params):
        self.loadcfg()
        self.printContain()
        