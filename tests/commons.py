'''
Module contains constants and utilities shared by test modules
'''

import logging
import threading
import os

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


from analyzer.utils import app

__unittest = True

WORK_FOLDER = os.path.join(app.DATA_FOLDER,'tests')
CHARS = "aáäbcčdďeéěëfghiíjklľmnňoóöpqrřsštťuúůüvwxyýzžAÁÄBCČDĎEÉĚËFGHIÍJKLMNŇOÓÖPQRŘSŠTŤUÚŮÜVWXYÝZŽ"

__initialized = False
__init_lock = threading.Lock()

def init():
    '''
    Initialization of test environment
    '''
    global __initialized
    global __init_lock
    if not __initialized:
        # avoid concurrent execution
        with  __init_lock:
            check_data_folder()
            # set logging to DEBUG level
            logging.basicConfig(level=logging.DEBUG)
            # block future reexecution
            __initialized = True


def check_data_folder(folder=""):
    if not os.path.exists(WORK_FOLDER):
        os.mkdir(WORK_FOLDER)
    path = os.path.join(WORK_FOLDER,folder)
    # check test data folder 
    if not os.path.exists(path):
        os.mkdir(path)



if __name__ == "__main__":
    print(f"!!! Module {os.path.basename(__file__)} is not built for direct execution !!!")
