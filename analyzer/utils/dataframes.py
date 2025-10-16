'''
This module provides utilities to make our programmer's live easier
'''
__version__ = "1.0.1"

import os
import io
import logging
import glob

import pandas as pd
import sqlalchemy as sql

from . import app
from .functions import ts_to_short,merge_into


log = logging.getLogger(__name__)
def log_dfs(dfs,msg="Actual DataFrames"):
    ''' write info and sample data from DataFrames '''
    log.info(msg)
    for key,df in dfs.items():
        log.info("DataFrame '%s': columns: %d, rows: %d",key,df.shape[1],df.shape[0])
        log.debug("DataFrame detail:%s",as_str(df))


def as_str(df):
    ''' print `pandas.DataFrame.info() into `str` '''
    buf = io.StringIO('\n')
    df.info(buf=buf)
    buf.write('\n')
    buf.write(f"{df}")
    return buf.getvalue()


def persist_dfs(dfs,**config):
    ''' write Pandas dataframes into DB

    All parameters are optional but if neither `app.CFGKEY_FILES`
    nor `app.CFGKEY_TABLES` and `app.CFGKEY_DBURI` is defined,
    no action is performed.

    Parameters
    ---------
    dfs: dict
        with labeled `DataFrames`
    files: dict
        file descriptors
    folder: pathlike
        optional source folder with files
    dburi: str
        DB URI including credentials
    tables: dict
        dict with persist target descriptors
    '''
    if len(dfs) == 0:
        log.warning("No DF to write; nothing to do")


    tmstmp = ts_to_short()
    
    for key,df in dfs.items():
        cfg = config.get(app.CFGKEY_OUTPUT)
        if cfg:
            file = cfg.get(key)
            #TODO if file == None
            if isinstance(file, str): # if string, create dict
                file = {app.CFGKEY_NAME: file, app.CFGKEY_CONFIG:{}}
            file = merge_into({},cfg.get(app.CFGKEY_CONFIG,{}),file)
            fpath = os.path.join(app.DATA_FOLDER,file.get(app.CFGKEY_FOLDER,app.OUTPUT_FOLDER),file.get(app.CFGKEY_FILENAME).format(timestamp=tmstmp))
            _,fext = os.path.splitext(fpath)
            log.debug("writing '%s' to file '%s'",key,fpath)
            try:
                match file.get(app.CFGKEY_FORMAT,fext[1:] if fext else 'csv').lower():
                    case 'csv':
                        log.debug("writing '%s' to CSV file '%s'",key,fpath)
                        df.to_csv(fpath,**file.get(app.CFGKEY_CONFIG,{}))
                    case 'xlsx':
                        log.debug("writing '%s' to XLSX file '%s'",key,fpath)
                        if not file.get(app.CFGKEY_CONFIG):
                            file[app.CFGKEY_CONFIG] = {}
                        if not file.get(app.CFGKEY_CONFIG).get('sheet_name'):
                            file.get(app.CFGKEY_CONFIG)['sheet_name'] = key
                        with pd.ExcelWriter(fpath,**({'mode':'a','if_sheet_exists':'replace'} if os.path.exists(fpath) else {})) as xlwr:
                            df.to_excel(xlwr,**file.get(app.CFGKEY_CONFIG,{}))
    
                log.info("Data frame '%s' has been written to '%s'",key,fpath)
            except Exception as err:
                log.warning("File writing error: '%s'",err,exc_info=log.isEnabledFor(logging.DEBUG))
    cfg = config.get(app.CFGKEY_DBOUT,{})
    dburi = cfg.get(app.CFGKEY_DBURI,config.get(app.CFGKEY_DBURI))
    if dburi and cfg:
        dburi = dburi.format(**{#app.CFGKEY_FOLDER:app.DATA_FOLDER,
                                app.CFGKEY_DBUSER: cfg.get(app.CFGKEY_DBUSER,config.get(app.CFGKEY_DBUSER,"")),
                                app.CFGKEY_DBPASS: cfg.get(app.CFGKEY_DBPASS,config.get(app.CFGKEY_DBPASS,""))
                            })
        # create connection to DB
        mdb = sql.create_engine(dburi)
        dbglobal = merge_into({},config.get(app.CFGKEY_CONFIG,{}),cfg.get(app.CFGKEY_CONFIG,{}))
        for key,df in dfs.items():
            if key != app.CFGKEY_CONFIG:
                if isinstance(cfg.get(key),str):
                    cfg[key] = {app.CFGKEY_NAME:cfg.get(key)}
                tbl_cfg = merge_into({},dbglobal,cfg.get(key,{}))
                log.debug("writing '%s' to table '%s'",key,tbl_cfg.get(app.CFGKEY_NAME,key))
                try:
                    if tbl_cfg.get(app.CFGKEY_BEFORE):
                        with mdb.connect() as dbcon:
                            dbcon.execute(sql.text(tbl_cfg.get(app.CFGKEY_BEFORE).format(table=tbl_cfg.get(app.CFGKEY_NAME,key))))
                    df.to_sql(tbl_cfg.get(app.CFGKEY_NAME,key),mdb,**tbl_cfg.get(app.CFGKEY_CONFIG,{}))
                    if tbl_cfg.get(app.CFGKEY_AFTER):
                        with mdb.connect() as dbcon:
                            dbcon.execute(sql.text(tbl_cfg.get(app.CFGKEY_AFTER).format(table=tbl_cfg.get(app.CFGKEY_NAME,key))))
                    log.info("Data frame '%s' has been written to '%s'",key,tbl_cfg.get(app.CFGKEY_NAME,key))
                except Exception as err:
                    log.warn("DB writing error: '%s' <%s>",err,dburi,exc_info=log.isEnabledFor(logging.DEBUG))
        mdb.dispose()


def build_dfs(**config):
    ''' read files into Pandas dataframe

    All parameters are optional but if neither `app.CFGKEY_FILES`
    nor `app.CFGKEY_SELECTS` and `app.CFGKEY_DBURI` is defined,
    no action is performed.

    Parameters
    ----------
    files: dict
        file descriptors
    folder: pathlike
        source folder with files
    queries: dict
        labeled queries (selects)
    dburi: str
        DB URI including credentials

    Returns
    -------
    dict: of dataframes labeled with `key` from configuration
    '''
    output = {}
    cfg = config.get(app.CFGKEY_SOURCE,{})
    for key,file in cfg.items():
        if key == app.CFGKEY_CONFIG:
            continue
        # check type of file
        if isinstance(file, str): # if string, create dict
            file = {app.CFGKEY_FILENAME: file, app.CFGKEY_CONFIG:{}}
        file = merge_into({},cfg.get(app.CFGKEY_CONFIG,{}),file)
        files = None
        fname = file.get(app.CFGKEY_FILENAME)
        if isinstance(fname,str):
            if fname.startswith('http'):
                files = [fname]
            else:
                fglob = os.path.join(app.DATA_FOLDER,file.get(app.CFGKEY_FOLDER,app.SOURCE_FOLDER),file.get(app.CFGKEY_FILENAME))
                log.debug("reading files '%s'",fglob)
                files = glob.glob(fglob)
        elif hasattr(fname, '__iter__'):
            files = fname
        else:
            raise ValueError(f"Filename expected `str` or Iterable, got '{type(file.get(app.CFGKEY_FILENAME))}'")
        if files:
            dfs = []
            for fpath in files: 
                try:
                    _,fext = os.path.splitext(fpath)
                    match file.get(app.CFGKEY_FORMAT,fext[1:] if fext else 'csv'):
                        case 'csv':
                            log.debug("reading '%s' to CSV file '%s'",key,fpath)
                            df = pd.read_csv(fpath,**file.get(app.CFGKEY_CONFIG,{}))
                        case 'xlsx':
                            log.debug("reading '%s' to XLSX file '%s'",key,fpath)
                            if not file.get(app.CFGKEY_CONFIG):
                                file[app.CFGKEY_CONFIG] = {}
                            if not file.get(app.CFGKEY_CONFIG).get('sheet_name'):
                                file.get(app.CFGKEY_CONFIG)['sheet_name'] = key
                            df = pd.read_excel(fpath,**file.get(app.CFGKEY_CONFIG,{}))

                    log.info("Got data from '%s': columns: %d, rows: %d",fpath,df.shape[1],df.shape[0])
                    log.debug("data sample:%s",as_str(df))
                    dfs.append(df)
                except Exception as err:
                    log.warn("File reading error: '%s'",err,exc_info=log.isEnabledFor(logging.DEBUG))
                    raise err
                
            output[key] = pd.concat(dfs,ignore_index=True)                    
        else:
            raise ValueError(f"No files '{fglob}' found")

    cfg = config.get(app.CFGKEY_DBSRC,{})
    dburi = cfg.get(app.CFGKEY_CONFIG,{}).get(app.CFGKEY_DBURI,config.get(app.CFGKEY_DBURI))
    if dburi and cfg:
        dburi = dburi.format(**{app.CFGKEY_FOLDER:app.DATA_FOLDER,
                                app.CFGKEY_DBUSER: config.get(app.CFGKEY_DBUSER,""),
                                app.CFGKEY_DBPASS: config.get(app.CFGKEY_DBPASS,"")
                            })
        # create connection to DB
        mdb = sql.create_engine(dburi)
        for key,query in cfg.items():
            if key == app.CFGKEY_CONFIG:
                continue
            if isinstance(query, str):
                query = {app.CFGKEY_SQL:query}
            # read data per query
            query[app.CFGKEY_CONFIG] = merge_into({},cfg.get(app.CFGKEY_CONFIG,{}).get(app.CFGKEY_CONFIG,{}),query.get(app.CFGKEY_CONFIG,{}))
            stmt = query.get(app.CFGKEY_SQL)
            log.debug("getting data '%s': %s",key,stmt)
            try:
                df = pd.read_sql_query(stmt, mdb,**query.get(app.CFGKEY_CONFIG,{}))
                log.info("Got data from '%s': columns: %d, rows: %d",key,df.shape[1],df.shape[0])
                #df.info()
                log.debug("data sample:%s",as_str(df))
                output[key] = df
            except Exception as err:
                log.warning("DB reading error: '%s' <%s>",err,dburi,exc_info=log.isEnabledFor(logging.DEBUG))
                raise err
        mdb.dispose()

    return output












#################################################################
##  Ochrana před přímým spuštěním souboru
if __name__ == "__main__":
    print(f"!!! Module {os.path.basename(__file__)} is not built for direct execution !!!")
