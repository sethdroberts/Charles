#Requires python3.6 or above
#Run the following commands to install modules:
    #pip3 install alpaca_trade_api
    #pip3 install websocket-client

import alpaca_trade_api as trade_api 
import time
import datetime 
import websocket
import json
import config as cfg
from sendsms import SendSMS as sms
import logging

logging.basicConfig(filename='darwin.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

APCA_API_KEY_ID = cfg.APCA_API_KEY_ID
APCA_API_SECRET_KEY = cfg.APCA_API_SECRET_KEY
APCA_API_BASE_URL = cfg.APCA_API_BASE_URL
ACCOUNT_URL = cfg.ACCOUNT_URL

POLYGON_API_KEY = APCA_API_KEY_ID
SOCKET = cfg.SOCKET

SECURITY = cfg.SECURITIES
CHANNEL = cfg.CHANNEL
TPROFIT = cfg.TPROFIT
SLOSS = cfg.SLOSS
EQ_PCT = 1/len(SECURITY)
TICKERS = ''

#Assemble tickers
a = 0
while a < len(SECURITY):
    TICKERS = TICKERS + CHANNEL + '.' + SECURITY[a]
    if a == len(SECURITY) - 1:
        a = a + 1
    else:
        TICKERS = TICKERS + ','
        a = a + 1

api = trade_api.REST(APCA_API_KEY_ID,\
APCA_API_SECRET_KEY,\
APCA_API_BASE_URL)

#Dictionary structure
clock = api.get_clock()
start_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
day_perform = []
current_positions = []
initiation = {}
top_change = []

#Returns seconds till market closes. Delayed by 1 seconds to prevent excessive API calls (only after portfolio built)
def time_till_close():
    clock = api.get_clock()
    closing_time = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    curr_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    time_till_close = int(closing_time - curr_time)
    time.sleep(1)
    return time_till_close

def time_till_open():
    clock = api.get_clock()
    open_time = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
    curr_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    time_till_open = int(open_time - curr_time)
    return time_till_open

def dictionary_filled():
    count = 0
    d = 0
    while d < len(day_perform):
        stock_perform = day_perform[d]
        price = stock_perform.get('current_price')
        if price == 0:
            status = 0
        else:
            status = 1
        count = count + status
        d = d + 1
    if count == len(day_perform):
        return True
    else:
        return False

def place_order(security, qty, side):
    api.submit_order(
    symbol = security,
    qty = qty,
    side = side,
    type = 'market',
    time_in_force = 'gtc')
    time.sleep(2)
    logging.debug('Placed order successfully')

def build_portfolio():
    g = 0
    while g < len(current_positions):
        logging.debug(g)
        order_data = current_positions[g]
        symbol = order_data.get('symbol')
        profit_price = float(order_data.get('profit_price'))
        loss_price = float(order_data.get('loss_price'))
        qty = int(order_data.get('qty'))
        logging.debug(symbol, profit_price, loss_price, qty)

        place_order(symbol, qty, 'buy')
        logging.info('Ordered {} shares of {}'.format(qty,symbol))
        logging.info('Take profit at {}. Stop loss at {}.'.format(profit_price,loss_price))
        g = g + 1

#Takes a dictionary and creates a bracket order for that
def change_position(data):
    security = data.get('symbol')
    logging.debug(security)
    profit_price = float(data.get('profit_price'))
    loss_price = float(data.get('loss_price'))
    qty = int(data.get('qty'))
    logging.debug(security, profit_price, loss_price, qty)
    place_order(security, qty, 'buy')

    logging.info('Ordered {} shares of {}'.format(qty,security))
    logging.info('Take profit at {}. Stop loss at {}.'.format(profit_price,loss_price))
    logging.info("==Equity transfer to {} complete==".format(security))

#Liquidates a position from a position_data file
def liquidate_position(data):
    security = data.get('symbol')
    logging.debug(security)
    qty = int(data.get('qty'))
    logging.debug(security, qty)
    place_order(security, qty, 'sell')

    logging.info('Liquidated {} shares of {}'.format(qty,security))

def performance():
    account = api.get_account()
    balance = float(account.equity)
    last_balance = float(account.last_equity)
    balance_change = round(balance - last_balance,2)
    percentage_change = round(((balance - last_balance)/last_balance * 100),2)
    return "Today's balance change: ${}. Today's percentage change: {}%".format(balance_change, percentage_change)

def on_open(ws):
    auth_data = {
    "action":"auth",
    "params":POLYGON_API_KEY
    }

    ws.send(json.dumps(auth_data))

    channel_data = {
    "action": "subscribe",
    "params": TICKERS
    }

    ws.send(json.dumps(channel_data))

    #Clear any existing dictionary data
    day_perform.clear()
    current_positions.clear()
    top_change.clear()
    initiation.clear()

    #Assembles initial dictionaries for each security
    b = 0
    while b < len(SECURITY):
        #Security list, day_perform, and current_positions are all in the same order
        day_perform.append({'symbol': SECURITY[b],'open_price': 0,'current_price': 0, 'day_change': 0})
        current_positions.append({'symbol': SECURITY[b], 'start_price': 0, 'profit_price': 0, 'loss_price': 0, 'qty': 0, 'equity': 0, 'status': 0})
        b = b + 1
    top_change.append({'symbol': SECURITY[0], 'change':0.01, 'price': 0})
    top_change.append({'symbol': SECURITY[1], 'change':0.001, 'price': 0})
    initiation.update({'initiation': 0, 'iteration': 0})
    #Liquidate any existing orders or positions
    api.cancel_all_orders()
    api.close_all_positions()
    time.sleep(2)
    logging.debug("==Liquidated all existing stock positions==")

def on_message(ws, message):
    global current_positions, top_change, initiation
    #Ensures no iterations during launch
    target_iterations = len(SECURITY) + 2
    count = initiation.get('iteration')
    if count < target_iterations:
        logging.debug(message)
        count = count + 1
        initiation.update({'iteration': count})

    else:
        #Update day_perform dictionary with current price and day change
        c = 0
        while c < len(SECURITY):
            security = SECURITY[c]
            data = json.loads(message)
            data = data[0]
            if data.get('sym') == security:
                stock_perform = day_perform[c]
                current_price = data.get('c')
                stock_perform.update({'current_price': current_price})
                if initiation.get('initiation') == 0:
                    stock_perform.update({'open_price': current_price})
                open_price = stock_perform.get('open_price')
                day_change = (current_price - open_price)/open_price * 100
                stock_perform.update({'day_change': day_change})

                #Update top_change list
                change_top = top_change[0]
                change_second = top_change[1]
                if security == change_top.get('symbol'):
                    change_top.update({'symbol': security, 'change': day_change, 'price': current_price})
                elif security == change_second.get('symbol'):
                    if day_change > change_top.get('change'):
                        change_second.update(change_top)
                        change_top.update({'symbol': security, 'change': day_change, 'price': current_price})
                    else:
                        change_second.update({'symbol': security, 'change': day_change, 'price': current_price})
                elif day_change > change_top.get('change'):
                    change_second.update(change_top)
                    change_top.update({'symbol': security, 'change': day_change, 'price': current_price})
                elif day_change > change_second.get('change'):
                    change_second.update({'symbol': security, 'change': day_change, 'price': current_price})
            c = c + 1

        #Ensures we don't start without dictionaries filled
        if dictionary_filled() == False:
            logging.debug('==Loading dictionaries===')

        elif initiation.get('initiation') == 0:
            account = api.get_account()
            equity = account.equity
            equity = float(equity)
            available = equity*EQ_PCT

            #Create initial positions in dictionary
            y = 0
            while y < len(current_positions):
                position_data = current_positions[y]
                perform_data = day_perform[y]
                price = float(perform_data.get('current_price'))

                profit_price = float(price*TPROFIT)
                loss_price = float(price*SLOSS)
                qty = int(available // price)

                position_data.update({'start_price': price})
                position_data.update({'profit_price': profit_price})
                position_data.update({'loss_price': loss_price})
                position_data.update({'qty': qty})
                position_data.update({'equity': available})
                position_data.update({'status': 1})
                logging.debug(position_data)
                y = y + 1
            logging.debug(current_positions)
            #Place orders for all initial positions
            if y == len(current_positions):
                logging.info('==Building portfolio==')
                build_portfolio()
                initiation.update({'initiation':1})
                logging.info('==Portfolio build completed==')
        elif time_till_close() > (60*35):
            #Check for prices beneath stoplosses
            logging.debug(top_change)
            e = 0
            while e < len(SECURITY):
                position_data = current_positions[e]
                perform_data = day_perform[e]
                security = position_data.get('symbol')

                price = float(perform_data.get('current_price'))
                loss_price = position_data.get('loss_price')
                profit_price = position_data.get('profit_price')
                status = position_data.get('status')
                logging.debug(security,price, profit_price, loss_price, status)

                if price > profit_price and status < 2:
                    logging.info('=={} hit 1%. Liquidating position=='.format(security))
                    liquidate_position(position_data)
                    position_data.update({'status': 2}) #Just to make sure the algo doesn't miss it if the price 
                    status = position_data.get('status')
                    logging.debug('Status is now {}'.format(status))
                    logging.info('==Liquidation complete==')
                    # profit_price = price*TPROFIT
                        # loss_price = price*SLOSS
                        # position_data.update({'start_price': price})
                        # position_data.update({'profit_price': profit_price})
                        # position_data.update({'loss_price': loss_price})
                        # logging.debug('==Hit take_profit for {}. Adjusting position data=='.format(security))


                #Find top-performing stock and move equity there. Update dictionary.
                elif price < loss_price or status == 0:
                    logging.debug('Position status of {} is {}'.format(security, status))
                    if status == 1:
                        liquidate_position(position_data)
                        position_data.update({'status': 0}) #Just to make sure the algo doesn't miss it if the price 
                        status = position_data.get('status')
                        logging.debug('Status is now {}'.format(status))

                    elif status == 0:
                        symbol = change_top.get('symbol')
                        change_top = top_change[0]
                        change_second = top_change[1]

                        logging.debug("This stock is {}. Top stock is {}. Top stock's change: {}. Second stock's change: {}".format(security, symbol, change_top.get('change'), change_second.get('change')))
                        
                        #Skip equity change if top stock isn't >0.1%. Prevents repeated stoploss.
                        if symbol == security and change_second.get('change') < 0.1:
                            logging.debug('==No alternative stocks above 0.0 percent for {}, skipping stoploss check=='.format(security))

                        elif change_top.get('change') < 0.1:
                            logging.debug('==No alternative stocks above 0.0 percent for {}, skipping stoploss check=='.format(security))
                        else:
                            available = float(position_data.get('equity'))
                            logging.debug(available)

                            change_top = top_change[0]
                            
                            if symbol == security:
                                change_second = top_change[1]
                                symbol = change_second.get('symbol')
                                logging.info('=={} fell below stoploss. Is already top stock. Moving equity to {}=='.format(security, symbol))
                                price = float(change_second.get('price'))
                            else:
                                logging.info('=={} fell below stoploss, moving equity to {}=='.format(security, symbol))
                                price = float(change_top.get('price'))
                            profit_price = price*TPROFIT
                            loss_price = price*SLOSS
                            logging.debug(symbol, price)
                            qty = int(available // price)
                            logging.debug(qty)
                            logging.debug(symbol, profit_price, loss_price, qty, price)

                            position_data.update({'symbol': symbol})
                            position_data.update({'start_price': price})
                            position_data.update({'profit_price': profit_price})
                            position_data.update({'loss_price': loss_price})
                            position_data.update({'qty': qty})
                            position_data.update({'equity': available})
                            position_data.update({'status': 1})
                            logging.debug(position_data)
                            logging.debug(current_positions)
                            change_position(position_data)
                    else:
                        pass
                e = e + 1
        else:
            logging.info("Market closing soon. Closing positions.")
            api.cancel_all_orders()
            api.close_all_positions()
            time.sleep(2)
            
            logging.info('===Final stock positions==')
            h = 0
            while h < len(current_positions):
                logging.info(current_positions[h])
                h = h + 1
            logging.info('==========================')
            result = performance()
            logging.info(result)
            sms.send_sms(result)

            day_perform.clear()
            current_positions.clear()
            top_change.clear()
            initiation.clear()

            logging.info('==Shutting down trading algorithm for the day===')
            time_to_close = time_till_close()
            time.sleep(time_to_close + 60)
            activate_algo()

def on_error(ws, error):
    logging.warning(error)

def on_close(ws):
    logging.critical('### closed ###')

ws = websocket.WebSocketApp(SOCKET,
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)

def activate_algo():
    if clock.is_open:
        ws.run_forever()

    else:
        time_to_open = time_till_open()
        logging.info('==Market is closed! It will open in {} seconds=='.format(time_to_open))
        time.sleep(time_to_open + 60)
        #Also add web scraper here and add securities. It will refresh every day.
        logging.info('==Launching trading algorithm==')
        ws.run_forever()

if __name__=="__main__":
    activate_algo()
