'''
This module provides
- shared constants
- global configuration
- info about execution environment
'''
__version__ = "0.0.1"

import os
import logging
import sys
import yaml
from pathlib import Path

#from analyzer.utils.functions import merge_into
from .functions import merge_into

APP_NAME = "DataAnalyzer"
APP_DESC = "Tréninková Aplikace pro analýzu dat. Cílem tréninku je základní seznámení s Python a nástrojem Pandas"

###############################################
# hlavni slozky aplikace
WORKING_FOLDER = os.getcwd()
''' active folder ''' 
FILE_FOLDER = os.path.dirname(__file__)
''' parent folder of the script '''
PROJECT_FOLDER = os.path.dirname(os.path.dirname(FILE_FOLDER))
''' project root folder '''
RESOURCE_FOLDER = os.path.join(PROJECT_FOLDER,'resource')
''' project static resources root folder '''
LOG_FOLDER = os.path.join(PROJECT_FOLDER,'log')
''' folder for log files '''
CONFIG_FOLDER = os.path.join(PROJECT_FOLDER,'config')
''' project configuration root folder '''
DATA_FOLDER = os.path.join(PROJECT_FOLDER,'data')
''' project data root folder '''
SOURCE_FOLDER = os.path.join(DATA_FOLDER,'source')
''' project source data root folder '''
OUTPUT_FOLDER = os.path.join(DATA_FOLDER,'output')
''' project source data root folder '''
WORK_FOLDER = os.path.join(DATA_FOLDER,'work')
''' project work data root folder '''
#############################################
# klice globalni konfigurace
CFGKEY_ARGS = 'args'
CFGKEY_LOGGER  = 'logger'
CFGKEY_LOGLEVEL = 'level'
CFGKEY_LOGFORMAT = 'format'
CFGKEY_SUBLOGS = 'children'
CFGKEY_LOGFILE = 'filename'
CFGKEY_FILE = 'file'
CFGKEY_NAME = 'name'
CFGKEY_USERNAME = 'user'
CFGKEY_FILENAME = 'filename'
CFGKEY_FOLDER = 'folder'
CFGKEY_CONFIG = 'config'
CFGKEY_FORMAT = 'format'
CFGKEY_SQL  = 'sql'
CFGKEY_LOGGING  = 'logger'
CFGKEY_IN = 'input'
CFGKEY_OUT = 'output'
CFGKEY_DBURI = 'dburi'
CFGKEY_DBUSER = 'dbuser'
CFGKEY_DBPASS = 'dbpwd'
CFGKEY_BEFORE = 'before'
CFGKEY_AFTER = 'after'
CFGKEY_FILES = 'files'
CFGKEY_SELECTS = 'selects'
CFGKEY_SOURCE = 'source'
CFGKEY_OUTPUT = 'output'
CFGKEY_DBSRC = 'dbsource'
CFGKEY_DBOUT = 'dboutput'
CFGKEY_WKHTML = 'wkhtml'
CFGKEY_STUDENT = 'student'


#############################################
# Nastaveni logovani
LOG_INFO_MSG = "%(asctime)s %(levelname)s: %(message)s"
''' format log zaznamu pro bezny log (pri behu programu) '''
LOG_DEBUG_MSG = "%(asctime)s [%(name)s] %(levelname)s: %(message)s (%(module)s.%(funcName)s:%(lineno)d)"
''' format log zaznamu pro log pri vyvoji aplikace '''
LOG_LEVEL = logging.DEBUG
''' vychozi uroven logovani pro aplikaci '''
LOG_FILE = f"{APP_NAME.lower()}.log"
''' vychozi jmeno log souboru '''


############################################
# globalni konfigurace
CONFIGURATION = {}


############################################
# funkcni cast modulu
def init_log(config={}):
    ''' zakladni nastaveni logovani
    - cile, kam budou zpravy zapisovany
    - format zapisovanych zprav
    '''
    # pokud neni receno v konfiguraci jinak, pouzij vychozi nastaveni urovne
    log_level = config.get(CFGKEY_LOGLEVEL,LOG_LEVEL)

    # formatovani logu z konfigurace nebo ... dokud programujeme, detail se hodi; hotova aplikace je strucnejsi
    log_format = config.get(CFGKEY_LOGFORMAT,LOG_DEBUG_MSG if log_level == logging.DEBUG else LOG_INFO_MSG)
    
    # zapis do souboru z konfigurace nebo se jmenem aplikace
    log_file = os.path.join(LOG_FOLDER,config.get(CFGKEY_LOGFILE,LOG_FILE))

    # zakladni konfigurace log systemu
    logging.basicConfig(
        level = log_level,
        format= log_format, 
        handlers=[
            logging.FileHandler(log_file,mode='w',encoding='utf-8'), 
            logging.StreamHandler(sys.stderr)   # vypis zprav na obrazovku; muzes vynechat, pokud nechces, aby aplikace psala na obrazovku
                                                # `sys.stderr` je vystup na obrazovku, ktery ostatni ostatni programy odlisit od bezneho vystupu
        ]
    )
    
    rootLogger = logging.getLogger()
    rootLogger.debug("active log level == %s",rootLogger.getEffectiveLevel())
    
    # konfigurace logovaci urovne pro konkretni logy
    for logname,level in config.get(CFGKEY_SUBLOGS,{}).items():
        lgr = logging.getLogger(logname)
        lgr.setLevel(level)
        lgr.debug("active log level == %s",lgr.getEffectiveLevel())
        
    return logging.getLogger(__name__)


def init(**config):
    ''' zakladni/globalni nastaveni pro aplikaci ''' 
    
    # nahrani konfigurace ze souboru
    global CONFIGURATION
    if not CONFIGURATION.get(CFGKEY_ARGS):
        CONFIGURATION[CFGKEY_ARGS] = config
    else:
        merge_into(CONFIGURATION.get(CFGKEY_ARGS),config)  # aktualizuj zakladni konfiguraci parametry funkce
    cfgfile = os.path.join(PROJECT_FOLDER,'config',f"{APP_NAME.lower()}.yml")
    if os.path.exists(cfgfile):  # pokud hlavni soubor s konfiguraci nacti ho
        fconfig  = {}
        with open(cfgfile,"r",encoding='utf-8') as cfgf:
            fconfig = yaml.safe_load(cfgf)
        merge_into(CONFIGURATION,fconfig)  # aktualizuj zakladni konfiguraci tou ze souboru 
    cfgfile = os.path.join(PROJECT_FOLDER,'config',config.get(CFGKEY_CONFIG,"just something crazy "))
    if os.path.exists(cfgfile):  # pokud najdes soubor s konfiguraci nacti ho
        fconfig  = {}
        with open(cfgfile,"r",encoding='utf-8') as cfgf:
            fconfig = yaml.safe_load(cfgf)
        merge_into(CONFIGURATION,fconfig)  # aktualizuj zakladni konfiguraci tou ze souboru 
    
    
    # overeni, ze existuji vsechny dulezite slozky
    # pokud neexistuji a nepodari se je vytvorit, aplikace skonci a vypise chybu 
    for folder in (DATA_FOLDER,SOURCE_FOLDER,OUTPUT_FOLDER,LOG_FOLDER):
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except Exception as err:
                print(f'ERROR: {err}')
                quit(2)    # ukonci program s `exit codem` s identifikaci chyby  
    
    log = init_log(CONFIGURATION.get(CFGKEY_LOGGER,{}))  # init logger s konfiguraci
    
    log.debug("Inicializace aplikace dokoncena")
    log.debug("Aktualni konfigurace aplikace:\n%s",yaml.dump(CONFIGURATION))    


def get_config(key=None):
    ''' vrati globalni konfiguraci nebo jeji cast '''
    output = CONFIGURATION
    if key:
        output = CONFIGURATION.get(key)
    return output

def get_arg(key=None):
    ''' vrati globalni argumenty nebo hodnotu zvoleneho '''
    output = CONFIGURATION.get(CFGKEY_ARGS)
    if key:
        output = output.get(key)
    return output






#################################################################
##  Ochrana před přímým spuštěním souboru
if __name__ == "__main__":
    print(f"!!! Module {os.path.basename(__file__)} is not built for direct execution !!!")
