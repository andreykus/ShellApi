# encoding: utf-8
'''
Created on 1 апр. 2017 г.
Настройка логирования
@author: av.Kustov
'''

import logging.handlers

#формат лога
filelog = logging.Formatter(fmt='%(asctime)s %(levelname)s:%(name)s: %(message)s '
    '(%(filename)s:%(lineno)d)',
    datefmt="%Y-%m-%d %H:%M:%S")
#обработчики логов - файл размером 1000000 байт , 5 файлов, затем переписыается
handlers = [
    logging.handlers.RotatingFileHandler('monitor.log', encoding='utf8',
        maxBytes=1000000, backupCount=5)
    #,logging.StreamHandler()
]

root_logger = logging.getLogger()
#уровень логирования
root_logger.setLevel(logging.DEBUG)

#регистрация обработчиков событий логирования
for handler in handlers:
    handler.setFormatter(filelog)
    handler.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    