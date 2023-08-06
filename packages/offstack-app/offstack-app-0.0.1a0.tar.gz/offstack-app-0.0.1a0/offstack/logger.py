import logging
import os

from logging.handlers import RotatingFileHandler
from offstack.constants import CONFIG_DIR

def logger():
    """Create the logger.
    """
    if not os.path.isdir(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
        
    formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    log = logging.getLogger("offstack")
    log.setLevel(logging.DEBUG)
    
    LOGFILE = os.path.join(CONFIG_DIR, "offstack.log")
    file_handler = RotatingFileHandler(LOGFILE, maxBytes=3145728, backupCount=1)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log

logger = logger()