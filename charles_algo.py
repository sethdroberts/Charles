import websocket
import json
import config as cfg
import logging
import scraper as s
import charles_functions as cf

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('charles.log')
logger.addHandler(file_handler)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)

#Dictionary structure
day_perform = []
current_positions = []
initiation = {}
top_change = []

#WARNING: Don't change this list without changing order_from_list function. It's default for all order inputs:
order_keys = ['symbol', 'qty', 'profit_price', 'loss_price']

#Clear all dictionaries
def clear_all():
    cf.clear(day_perform)
    cf.clear(current_positions)
    cf.clear(initiation)
    cf.clear(top_change)

#Places an order based on a list of data
def order_from_list(list, side):
    symbol = list[0]
    qty = list[1]
    profit_price = list[2]
    loss_price = list[3]
    cf.place_order(symbol, qty, side)
    if side == 'buy':
        logging.info('Ordered {} shares of {}'.format(qty,symbol))
        logging.info('Take profit at {}. Stop loss at {}.'.format(profit_price,loss_price))
    else:
        logging.info('Liquidated {} shares of {}'.format(qty,symbol))

#Places order based on dictionary and list of keys to extract
def change_position(dict, keys_list):
    order_data = cf.multiple_listdict(dict, keys_list)
    symbol = order_data[0]
    order_from_list(order_data, 'buy')
    logging.info("==Equity transfer to {} complete==".format(symbol))

#Places orders for all lists of order variables in list of lists
def build_portfolio(list, keys_list):
    order_list = cf.build_values_list(list, keys_list)
    x = 0
    while x < len(order_list):
        order_data = order_keys[x]
        order_from_list(order_data, 'buy')
    x += 1

#Liquidates a position from a dictionary item
def liquidate_position(dict, keys_list):
    order_data = cf.multiple_listdict(dict, keys_list)
    order_from_list(order_data, 'sell')
    
def on_open(ws):
    auth_data = {
    "action":"auth",
    "params":cfg.POLYGON_API_KEY
    }

    ws.send(json.dumps(auth_data))

    channel_data = {
    "action": "subscribe",
    "params": s.assemble_tickers(cfg.SECURITIES)
    }

    ws.send(json.dumps(channel_data))

    clear_all()

def on_message(ws, message):
    logger.info(message)

def on_error(ws, error):
    logger.warning(error)

def on_close(ws):
    logger.critical('### closed ###')

ws = websocket.WebSocketApp(cfg.SOCKET,
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)