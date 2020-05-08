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
    percentage_change = round(percent_change(float(account.equity), float(account.last_equity)),2)
    # percentage_change = round(((float(account.equity) - float(account.last_equity))/float(account.last_equity) * 100),2)
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

def percent_change(start_val, end_val):
    percent_change = (end_val - start_val)/start_val * 100
    return percent_change

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

#Creates a dictionary from a list of keys. Adds to a list, all initalized at 0.001 (to avoid dividing by zero)
def create_dict(key_list):
    dict = {}
    x = 0
    while x < len(key_list):
        dict.update({key_list[x]: 0.001})
        x += 1
    return dict

#Takes an empty list. For each value in second list, creates a dictionary with the keys in the first list.
#Initializes all to 0 except the first variable, which is initialized to the init variable.
#Returns the completed list.
def assemble_dicts(empty_list, key_list, init_list):
    x = 0
    while x < len(init_list):
        new_dict = create_dict(key_list)
        new_dict.update({key_list[0]: init_list[x]})
        empty_list.append(new_dict)
        x += 1
    return empty_list

initiation = {}
initiation.update({'initiation': 0})

#Updates a dict with ws data
def update_perform(data, dict):
    dict.update({'current_price': data.get('c')})
    if initiation.get('initiation') == 0:
        data.update({'open_price': data.get('c')})
    dict.update({'day_change': percent_change(dict.get('open_price'), data.get('c'))})
    return dict

#
def update_top_change(data, dict):
    pass

#Updates a dictionary with message from websocket
#Will have to move to websocket
def update_ws_dict(data, dict_list):
    data = json.loads(data)
    data = [0]
    x = 0
    while x < len(dict_list):
        security = cfg.SECURITIES[x]
        if security == data.get('sym'):
            pass


# c = 0
# while c < len(SECURITY):
#             security = SECURITY[c]
#             data = json.loads(message)
#             data = data[0]
#             if data.get('sym') == security:
#                 stock_perform = day_perform[c]
#                 current_price = data.get('c')
#                 stock_perform.update({'current_price': current_price})
#                 if initiation.get('initiation') == 0:
#                     stock_perform.update({'open_price': current_price})
#                 open_price = stock_perform.get('open_price')
#                 day_change = (current_price - open_price)/open_price * 100
#                 stock_perform.update({'day_change': day_change})

#                 #Update top_change list
#                 change_top = top_change[0]
#                 change_second = top_change[1]
#                 if security == change_top.get('symbol'):
#                     change_top.update({'symbol': security, 'change': day_change, 'price': current_price})
#                 elif security == change_second.get('symbol'):
#                     if day_change > change_top.get('change'):
#                         change_second.update(change_top)
#                         change_top.update({'symbol': security, 'change': day_change, 'price': current_price})
#                     else:
#                         change_second.update({'symbol': security, 'change': day_change, 'price': current_price})
#                 elif day_change > change_top.get('change'):
#                     change_second.update(change_top)
#                     change_top.update({'symbol': security, 'change': day_change, 'price': current_price})
#                 elif day_change > change_second.get('change'):
#                     change_second.update({'symbol': security, 'change': day_change, 'price': current_price})
#             c = c + 1


#   b = 0
#     while b < len(SECURITY):
#         #Security list, day_perform, and current_positions are all in the same order
#         day_perform.append({'symbol': SECURITY[b],'open_price': 0,'current_price': 0, 'day_change': 0})
#         current_positions.append({'symbol': SECURITY[b], 'start_price': 0, 'profit_price': 0, 'loss_price': 0, 'qty': 0, 'equity': 0, 'status': 0})
#         b = b + 1
#     top_change.append({'symbol': SECURITY[0], 'change':0.01, 'price': 0})
#     top_change.append({'symbol': SECURITY[1], 'change':0.001, 'price': 0})
#     initiation.update({'initiation': 0, 'iteration': 0})

perform_keys = ['symbol','open_price', 'current_price', 'day_change']
# position_keys = ['symbol', 'start_price', 'profit_price', 'loss_price', 'qty', 'equity']
# top_keys = ['symbol', 'change', 'price']
# initiation_keys = ['initiation']

# current_positions = []
day_perform = []
# top_change = []
# initiation = {}

# initiation.update({initiation_keys[0]: 0})

# # assemble_dicts(current_positions, perform_keys, cfg.SECURITIES)
assemble_dicts(day_perform, perform_keys, cfg.SECURITIES)
# # assemble_dicts(top_change, perform_keys, cfg.SECURITIES[:2])
# # initiation = create_dict(initiation_keys)

# # print(current_positions)
print(day_perform)
# # print(top_change)
# # print(initiation)

# print(initiation)

new_dict = {'c': 234}

print(update_perform(new_dict, day_perform[0]))