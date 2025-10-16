'''
Test zakladnich funkci aplikace
'''

import os
import datetime
import pandas
import random
import logging
import unittest
import shutil
import yaml
import re
#import pdfkit
import requests
#import weasyprint
import sqlalchemy as sql
from functools import reduce

import commons
from analyzer.utils import app, functions,dataframes

#block print of traceback with assert/fail messages
__unittest = True
__module__ = os.path.splitext(os.path.basename(__file__))[0]


CFGKEY_DBCFG = 'sql'

KEY_TIMESTAMP = 'dtm'
KEY_DICEGAME = 'dicegame'
KEY_DICE1 = 'dc1'
KEY_DICE2 = 'dc2'
KEY_DICE3 = 'dc3'
KEY_DICE4 = 'dc4'
KEY_DICE5 = 'dc5'
KEY_DICE6 = 'dc6'
KEY_MESSAGE = 'msg'
KEY_VALUE = 'val'
KEY_FLOW = 'flow'


DATA_PATH = os.path.join(commons.WORK_FOLDER,__module__)

log = logging.getLogger(__module__)

def build_ref_dfs():
    dicegame = []
    flow = []
    now = datetime.datetime.now()
    fval = 100.0

    for ii in range(0,20):
        tmstmp = pandas.to_datetime(now + datetime.timedelta(minutes=ii)).round("1s")
        dicegame.append({
                KEY_TIMESTAMP: tmstmp,
                KEY_DICE1: random.randint(1,6),
                KEY_DICE2: random.randint(1,6),
                KEY_DICE3: random.randint(1,6),
                KEY_DICE4: random.randint(1,6),
                KEY_DICE5: random.randint(1,6),
                KEY_DICE6: random.randint(1,6),
            })

        msg = []
        for jj in range(0,random.randint(4,10)):
            msg.append(reduce(lambda x,y:x+y,random.sample(commons.CHARS,random.randint(4,10))))

        fval = fval * (0.8+random.random()*0.4)
        flow.append({
                KEY_TIMESTAMP: tmstmp,
                KEY_MESSAGE: ' '.join(msg),
                KEY_VALUE: random.random() * 100,
                KEY_FLOW: fval
            })

    output = {
            KEY_DICEGAME: pandas.DataFrame(dicegame),
            KEY_FLOW: pandas.DataFrame(flow)
        }

    return output


class TestAppFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(DATA_PATH):
            try:
                shutil.rmtree(DATA_PATH)
            except Exception as err:
                log.warning("Unable to clear folder '%s': %s",DATA_PATH,err)
        commons.check_data_folder(DATA_PATH)
        with open(os.path.join(app.CONFIG_FOLDER,'keys.yml'),'r') as kf:
            cls.__keys = yaml.safe_load(kf)

    @classmethod
    def tearDownClass(cls):
        #shutil.rmtree(DATA_PATH)
        pass
    

    def check_db_access(self):
        dburi = re.sub(r"([^:]+://)[^@]+(@.*)",r"\1{dbuser}:{dbpwd}\2",self.__keys.get(app.CFGKEY_DBURI))
        for usr in ('robot','student'):
            with self.subTest(f"DB_access_{usr}"):
                try:
                    sqldb = sql.create_engine(dburi.format(dbuser=usr,dbpwd=app.get_config(app.CFGKEY_SQL).get(app.CFGKEY_STUDENT)))
                    pandas.read_sql_table("py_dbtest1",sqldb)
                    pandas.read_sql_table("py_dbtest2",sqldb)
                except Exception as err:
                    log.warning("Access to DB for '%s' doesn't work '%s'",usr,str(err).split('\n')[0])


    def test_io(self):
        '''
        Test functions `functions.persist_dfs` and `functions.build_dfs`
        '''
        ref = build_ref_dfs()
        dburi = self.__keys.get(app.CFGKEY_DBURI)
        for key,val in [
                        ('csv',app.get_config('csv')),
                        ('excel',app.get_config('excel')),
                        ('sql',{**app.get_config('sql'),app.CFGKEY_DBURI: dburi})
                    ]:
            with self.subTest(f"IO_test_{key}"):
                log.info("IO: Creating '%s' output ...",key)
                dataframes.persist_dfs(ref,**val,**{app.CFGKEY_LOGGER:log})
                log.info("Reading '%s' input ...",key)
                tst = dataframes.build_dfs(**val,**{app.CFGKEY_LOGGER:log})
                log.info("Comparing dataframes ...")
                for dfid,df in ref.items():
                    log.info("DF: '%s'",dfid)
                    pandas.testing.assert_frame_equal(df,tst.get(dfid))
                log.info("IO: '%s' OK",key)
        self.check_db_access()
        pass
        

    def _test_pdf(self):
        '''
        Test export to PDF
        '''
        ref = build_ref_dfs()
        tohtml = "<html><body>\n"
        for key,df in ref.items():
            tohtml += df.to_html(table_id=key)
        tohtml += "</body></html>"
        html = os.path.join(DATA_PATH,'tables.html')
        with open(html,mode='w',encoding='utf-8') as hf:
            hf.write(tohtml)
        log.info("HTML export to '%s' OK",html)


        pdf = os.path.join(DATA_PATH,'tables.pdf')
        # pdfconfig = pdfkit.configuration(wkhtmltopdf=app.get_config('wkhtml'))
        # pdfkit.from_file(html,pdf,configuration=pdfconfig)
        topdf = weasyprint.HTML(html,encoding='utf-8')
        topdf.write_pdf(pdf)
        log.info("PDF export to '%s' OK",pdf)

    def test_robot_registration(self):
        data = {
            'conn_name': self.__keys.get(app.CFGKEY_USERNAME),
            'conn_string': re.sub(r"([^:]+://)[^@]+(@.*)",r"\1{dbuser}:{dbpwd}\2",self.__keys.get(app.CFGKEY_DBURI))
        }
        requests.post('https://development.techniarch.com/pcsda/robot.php?register',data=data)


if __name__ == "__main__":
    app.init(config=f"{__module__}.yml")
    try:
        #config = app.CONFIGURATION.get(CFGKEY_DBCFG)
        test = unittest.main(TestAppFunctions(),exit=False)
        if len(test.result.errors)>0 or len(test.result.failures)>0:
            raise RuntimeError(f'Pocet chyb {len(test.result.errors)+len(test.result.failures)}')
    except Exception as err:
        print('\033[91m' + "\nNeco neni v poradku:",err,'\033[0m')
    else:
        print('\033[92m' + "\nVse pripraveno ;-)" + '\033[0m')

    print("\n"*2)

