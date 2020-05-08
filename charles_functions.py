#This file holds all the functions used in the other scripts
import config as cfg
import datetime
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('charles.log')
logger.addHandler(file_handler)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)

#Places an Alpaca order with certain input criteria
def place_order(security, qty, side):
    api = cfg.api
    api.submit_order(
    symbol = security,
    qty = qty,
    side = side,
    type = 'market',
    time_in_force = 'gtc')
    time.sleep(2)
    logger.debug('==Placed order successfully==')

def performance():
    api = cfg.api
    account = api.get_account()
    balance_change = round(float(account.equity) - float(account.last_equity),2)
    percentage_change = round(((float(account.equity) - float(account.last_equity))/float(account.last_equity) * 100),2)
    return "Today's balance change: ${}. Today's percentage change: {}%".format(balance_change, percentage_change)

def liquidate_all():
    api = cfg.api
    api.cancel_all_orders()
    api.close_all_positions()
    time.sleep(2)
    logging.debug("==Liquidated all existing stock positions==")

#Returns get_clock
def get_clock():
    api = cfg.api
    return api.get_clock()

#True if market is open; else False
def clock_is_open():
    clock = get_clock()
    return clock.is_open

#Returns current time in seconds
def curr_time():
    clock = get_clock()
    curr_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    return curr_time

#Returns next closing time in seconds
def closing_time():
    clock = get_clock()
    closing_time = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    return closing_time

#Returns next open time in seconds
def open_time():
    clock = get_clock()
    open_time = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
    return open_time

#Returns time till next close in seconds
def time_till_close():
    time_till_close = closing_time() - curr_time()
    return time_till_close

#Returns time till next open in seconds
def time_till_open():
    time_till_open = open_time() - curr_time()
    return time_till_open

#Clears a list or dictionary
def clear(list):
    list.clear()

#Returns the value of a key in a dictionary
def dict_val(dict, key):
    return dict.get(key)

#Returns the value of a key in a dictionary at an index # of a list
def get_listdict_val(list, index, key):
    dict = list[index]
    return dict_val(dict, key)

#Returns 0 if value = 0, or 1 if nonzero
def non_zero(value):
    if value == 0:
        return 0
    else:
        return 1

#Returns True if all dictionaries in a list have a non-zero value for a key
def dictionary_filled(list, key):
    count = 0
    x = 0
    while x < len(list):
        value = get_listdict_val(list, x, key)
        status = non_zero(value)
        count += status
        x = x + 1
    if count == len(list):
        return True
    else:
        return False

#Returns the values of all keys in keys_list in a given dictionary
def multiple_listdict(dict, keys_list):
    values_list = []
    x = 0
    while x < len(keys_list):
        value = dict_val(dict, keys_list[x])
        values_list.append(value)
        x += 1
    return values_list

#Takes a list of dictionaries and a list of keys to be found
#Returns a list of lists with the key values for each item
def build_values_list(list, keys_list):
    list_of_lists = []
    x = 0
    while x < len(list):
        values = multiple_listdict(list[x], keys_list)
        list_of_lists.append(values)
        x = x + 1
    return list_of_lists



# stuff = {'item': 3, 'bottle': 'string'}
# things = {'item': 2, 'bottle': 52.0}
# others = {'item': 6, 'bottle': 2}
# fun = {'item': 0, 'bottle': 50}
# winning = [stuff, things, others, fun]

# list_of_keys = ['item', 'bottle']

# print(build_values_list(winning, list_of_keys))

# dict = {}

# stuff = {'stuff': 3}
# things = {'things': 2}
# others = {'others': 6}
# fun = {'item': 0}

# dict.update(stuff)
# dict.update(things)
# dict.update(others)
# dict.update(fun)

# # print(dict)

# # winning = [stuff, things, others, fun]

# item = 'item'
# stuff = 'stuff'
# things = 'things'
# others = 'others'

# big_list = []
# big_list.append(item)
# big_list.append(stuff)
# big_list.append(things)

# # print(big_list)
# # print(dict)

# print(multiple_listdict(dict, big_list))

# # # print(stuff)
# # # print(things)
print(performance())