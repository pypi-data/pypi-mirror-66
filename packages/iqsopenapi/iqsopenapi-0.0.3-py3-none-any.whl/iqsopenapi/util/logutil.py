# -*- coding: utf-8 -*-
import sys
import time
import logging
from datetime import datetime

logger = logging.getLogger('iqsopenapilogger')
logger.setLevel(logging.INFO)

logformat = logging.Formatter('%(asctime)-15s %(levelname)s [%(filename)s:%(lineno)d] %(message)s')

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logformat)
logger.addHandler(console_handler)

__add_logfile = False


def log2file():
    global __add_logfile
    if __add_logfile:
        return

    file_handler = logging.FileHandler('openapi_{}.log'.format(datetime.now().strftime("%Y%m%d%H%M%S")))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logformat)
    logger.addHandler(file_handler)
    __add_logfile = True

if __name__ == '__main__':
    
    log2file();

    logger.error("test error")
    logger.critical("test critical")
    logger.debug("test debug")
    logger.info("test info")