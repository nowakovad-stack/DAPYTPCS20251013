'''
Demonstration how to built Python unit tests
'''

import unittest
import logging
from copy import deepcopy

import commons

#get logger
log = logging.getLogger(__name__)
#block print of traceback with assert/fail messages
__unittest = True

class DemoTest(unittest.TestCase):
    '''
    Demo unit test class
    '''

    @classmethod
    def setUpClass(cls):
        commons.init()

    def test_dict_reference(self):
        '''
        Create reference to dictA and update both.

        Expected: mutation of one dict propagates to the other
        '''
        log.info("Testing update of referenced dicts ...")
        dictA = dict(a=1, b=2, c=3)
        log.debug("dictA before update: %s",dictA)
        dictB = dictA
        dictA['a'] = 11
        dictB['c'] = 33
        log.debug("dictA after update: %s",dictA)
        assert  dictA['c'] == 33 and dictB['a'] == 11, "dict update failed"
        log.info("Test of update of referenced dicts done.")


    def test_dict_deepcopy(self):
        '''
        Create deepcopy of dictA and update both.

        Expected: both dicts are independent on mutations
        '''
        log.info("Testing update of independent dicts ...")
        dictA = dict(a=1, b=2, c=3)
        log.debug("dictA before update: %s",dictA)
        dictB = deepcopy(dictA)
        dictA['a'] = 11
        dictB['c'] = 33
        log.debug("dictA after update: %s",dictA)
        assert  dictA['c'] == 3 and dictB['a'] == 1, "dict update failed"
        log.info("Test of update of independent dicts done.")


    def test_subtest(self):
        '''
        Check range of numbers and pass if numbers is odd
        '''
        log.info("Testing using subtests ...")
        for ii in range(0,9):
            with self.subTest(f"is {ii} odd?"):
                if (ii % 2) == 0:
                    log.debug("Number '%d' is even => FAIL",ii)
                    self.fail(f"{ii} is even")
                else:
                    log.debug("Number '%d' is odd => OK",ii)
        log.info("Test with subtests done.")
