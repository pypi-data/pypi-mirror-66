import logging

class Log(object):
    def __init__(self,level,path):
        self.level = level
        self.path = path

    @staticmethod
    def get_instance(level,path):
        return Log(level=level,path=path)

    import enum
    class Levels(enum.Enum):
        INFO = logging.INFO
        WARNING = logging.WARNING
        ERROR = logging.ERROR
        CRITICAL = logging.CRITICAL
        NOTSET = logging.NOTSET

class SDKLogger(object):
    def __init__(self,level,path):
        logger = logging.getLogger('client_lib')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(filename)s - %(funcName)s - %(lineno)d  - %(message)s')
        console_handler = logging.StreamHandler()
        if path is not None:
            file_handler = logging.FileHandler(path)
            file_handler.setLevel(level.name)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            console_handler.setLevel(level.name)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    @staticmethod
    def initialize(level,path):
        SDKLogger(level=level,path=path)

