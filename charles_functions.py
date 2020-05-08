#This file holds all the functions used in the other scripts
import config as cfg
import datetime
import time
    
def get_clock():
    api = cfg.api
    return api.get_clock()

def clock_is_open():
    clock = get_clock()
    return clock.is_open

def curr_time():
    clock = get_clock()
    curr_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    return curr_time

def closing_time():
    clock = get_clock()
    closing_time = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    return closing_time

def open_time():
    clock = get_clock()
    open_time = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
    return open_time

def time_till_close():
    time_till_close = closing_time() - curr_time()
    return time_till_close

def time_till_open():
    time_till_open = open_time() - curr_time()
    return time_till_open

    

print(time_till_open())
print(time_till_close())