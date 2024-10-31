import os
import logging
from logging import handlers
from backend.config import LOG_LEVEL, BASE_DIR


def init_logging(logger_name=None, stream=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)

    sh = logging.StreamHandler(stream=stream)
    fh = logging.handlers.TimedRotatingFileHandler(filename=BASE_DIR + '/log/logs.log',
                                                   when='h',
                                                   interval=24,
                                                   backupCount=7,
                                                   encoding="utf-8")
    fmt = "[%(asctime)s %(levelname)s %(threadName)s %(filename)s %(funcName)s %(lineno)d] [%(thread)d] [%(message)s]"
    formatter = logging.Formatter(fmt)

    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger

