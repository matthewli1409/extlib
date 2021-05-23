import logging
import os

APP_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level='INFO', format='%(message)s', datefmt='%d/%m/%y %H:%M:%S')

logger = logging.getLogger('__name__')
logger.propagate = 0
logger.setLevel(logging.DEBUG)

s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)

f_handler = logging.FileHandler(os.path.join(APP_ROOT_PATH, '../..', 'log', 'log.log'))
f_handler.setLevel(logging.DEBUG)

s_format = logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
f_format = logging.Formatter('%(asctime)s %(levelname)s -: %(module)s.%(funcName)s -: %(message)s', '%Y-%m-%d %H:%M:%S')

s_handler.setFormatter(s_format)
f_handler.setFormatter(f_format)

logger.addHandler(s_handler)
logger.addHandler(f_handler)

errorslogger = logging.getLogger('errorslogger')
errorslogger.propagate = False
errorshandler = logging.FileHandler(os.path.join(APP_ROOT_PATH, '../..', 'log', 'errors.log'))
f_format = logging.Formatter('%(asctime)s %(levelname)s -: %(module)s.%(funcName)s -: %(message)s', '%Y-%m-%d %H:%M:%S')
errorshandler.setFormatter(f_format)
errorslogger.addHandler(errorshandler)
