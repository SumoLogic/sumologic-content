'''
    Sumologic API Python Client
'''
from sumologic.api import content, folder, permission
import logging


LOGGER_NAME = 'sumologic'
LOG_FORMAT = '%(asctime)-15s %(levelname)-5s [module=%(module)s] %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)
