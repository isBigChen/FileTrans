import sys
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(asctime)s] [%(filename)s:%(module)s:%(lineno)d] %(levelname)s %(message)s',)
logger = logging.getLogger()