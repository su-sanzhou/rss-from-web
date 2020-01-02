import logging
from logging.handlers import RotatingFileHandler
import config

class RssLog(object):
    def __init__(self):
        self.rss_log_file = config.get_other_config()["log_file"]

        self.rss_logger = logging.getLogger("rss")
        self.rss_logger.setLevel(logging.INFO)

        file_handler = RotatingFileHandler(self.rss_log_file,
                                           mode='w',
                                           maxBytes=1000,
                                           backupCount=3,
                                           encoding='utf-8')

        formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.rss_logger.addHandler(file_handler)

        #useage
        #self.rss_logger.info('info messages')