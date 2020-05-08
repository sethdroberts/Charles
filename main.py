import time
import config as cfg
import charles_functions as c
import scraper as s
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
        print('run algo')

    else:
        time_to_open = c.time_till_open()
        logger.info('==Market is closed! It will open in {} seconds=='.format(time_to_open))
        time.sleep(time_to_open + 60)
        # TICKERS = s.assemble_tickers(cfg.SECURITIES)
        logger.info('==Launching trading algorithm==')
        print('run algo -- pass TICKERS into algo. WIll be useful later on')

if __name__=="__main__":
    activate_algo()
