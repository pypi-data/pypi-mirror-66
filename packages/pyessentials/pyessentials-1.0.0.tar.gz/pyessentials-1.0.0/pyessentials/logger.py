import logging

class Logger:
    def __init__(self, file, enable = True):
        self.enable = enable
        if self.enable:
            logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s [%(levelname)s] %(message)s', handlers = [logging.FileHandler(file), logging.StreamHandler()])

    def critical(self, message):
        if self.enable:
            logging.critical(message)

    def warning(self, message):
        if self.enable:
            logging.warning(message)

    def info(self, message):
        if self.enable:
            logging.info(message)

    def debug(self, message):
        if self.enable:
            logging.debug(message)