import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logging():

    if not os.path.exists('logs'):
        os.makedirs('logs')
    handler = TimedRotatingFileHandler("logs/app.log", when="midnight", interval=1)

    log = logging.getLogger("app")
    handler.suffix = "%Y%m%d"
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
