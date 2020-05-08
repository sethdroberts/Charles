import time
import config as cfg
import charles_functions as c
from charles_algo import ws
import logging
# from scraper import Scavenger as s
# import socket

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('charles.log')
logger.addHandler(file_handler)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)

def activate_algo():
    if c.clock_is_open():
        ws.run_forever()

    else:
        time_to_open = c.time_till_open()
        logger.info('==Market is closed! It will open in {} seconds=='.format(time_to_open))
        # time.sleep(time_to_open + 60)
        logger.info('==Launching trading algorithm==')
        ws.run_forever()

if __name__=="__main__":
    activate_algo()
