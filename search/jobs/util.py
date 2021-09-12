import logging

def init_logger(name: str = None, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name=name)
    level = level.upper()
    if level == "NOTSET":
        llevel = logging.NOTSET
    elif level == "DEBUG":
        llevel = logging.DEBUG
    elif level == "INFO":
        llevel = logging.INFO
    elif level == "WARN":
        llevel = logging.WARN
    elif level == "WARNING":
        llevel = logging.WARNING
    elif level == "ERROR":
        llevel = logging.ERROR
    elif level == "FATAL":
        llevel = logging.FATAL
    elif level == "CRITICAL":
        llevel = logging.CRITICAL
    logger.setLevel(llevel)
    return logger