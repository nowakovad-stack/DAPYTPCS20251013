'''
This module provides utilities to make our programmer's live easier
'''
__version__ = "1.0.1"

import os
import random
import string
import time
import logging
import pytz
import copy
import datetime
import re


ALPHABET = string.ascii_letters + string.digits

log = logging.getLogger(__name__)

def uuid_short(k=8):
    ''' generate unique random string '''
    return "".join(random.choices(ALPHABET,k=k))


def uuid_num():
    ''' generate unique number '''
    return int(time.time()*10000000000)+random.randrange(1000)


def to_ascii(text):
    ''' replace diacritics in text with ASCII
    '''
    chars_from = 'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ'
    chars_to  =  'AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs'
    output = ""
    for chr in text:
        pos = chars_from.find(chr)
        if pos < 0:
            output += chr
        else:
            output += chars_to[pos]
    return output


def name2id(name,pattern=(r'^(\w{1,4})\w*\s+(\w{1,4})\w*',r'\1\2')):
    ''' Generate ID from name using REGEXP replace '''
    name = to_ascii(name).lower()
    output = re.sub(pattern[0],pattern[1],name)
    return output


def merge_into(base, *updates):
    '''
    Recursively merge dictionaries into 'base'. To ensure consistency of updates the procedure creates deepcopy of them

    Parameters
    ----------
    base: dict
        all keys are copied to output
    updates: dicts
        update all values for existing keys and insert non-existing keys

    Returns
    -------
    dict:
        new dictionary with merged/updated values

    Raises
    ------
    TypeError
        if type of values with the same key is not equal
    ValueError
        if `deepcopy` of any item fails
    '''
    output = base
    for update in updates:
        withErr = False
        if isinstance(update,dict): #simply ignore non dictionary updates
            errors = []
            for key,value in update.items():
                if not output.get(key):
                    output[key] = copy.deepcopy(value)
                else:
                    if type(output.get(key)) == type(value):
                        if isinstance(value,dict):
                            output[key] = merge_into(output.get(key),value)
                        elif isinstance(value,list):
                            for item in value:
                                if not item in output.get(key):
                                    try:
                                        output.get(key).append(copy.deepcopy(item))
                                    except:
                                        raise ValueError(f"Unable to create deepcopy of source: {item}")
                        elif isinstance(value,set):
                            output[key] |= value
                        else:
                            output[key] = copy.deepcopy(value)
                    else:
                        withErr = True
                        errors.append(f"type(base[{key}]) = {type(output.get(key))} while type(update[{key}]) = {type(update.get(key))}")
        if withErr:
            raise TypeError("Type of source and destination is not equal: "
                                        + ", ".join(errors))
    return output


def ts_to_short(timestamp = time.time(), timezone = pytz.utc):
    '''
    Convert `timestamp` to 'condensed' string "%Y%m%d%H%M%S", without TZ indication

    Parameters
    ----------
    timestamp: float
        (default `time.time()`)

    timezone
        (default `pytz.utc`)

    Returns
    -------
    str
        date time in `%Y%m%d%H%M%S` format

    '''
    return datetime.datetime.fromtimestamp(timestamp).astimezone(timezone).strftime("%Y%m%d%H%M%S")















if __name__ == "__main__":
    print(f"!!! Module {os.path.basename(__file__)} is not built for direct execution !!!")
