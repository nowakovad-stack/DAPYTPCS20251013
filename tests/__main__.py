'''
Executes test defined as argument or all tests in this package
'''

# Import system modules
import unittest
import logging
import sys
import os

import commons

## Discover and execute tests
def exec_tests(start_dir: str = '.', pattern: str = 'Test*.py'):
	suite = unittest.TestLoader().discover(start_dir,pattern)
	unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
	# rootlogger = logging.getLogger()
	# rootlogger.setLevel(logging.DEBUG)

	# for key,fldr in commons.FOLDERS.items():
	# 	rootlogger.debug("Checking folder %s ...",key)
	# 	commons.check_folder(fldr)

	# rootlogger.addHandler(commons.get_log_file_handler("tests.log",commons.FILE_LOG_MSG))
	if len(sys.argv) > 1:
		exec_tests(os.path.dirname(__file__),sys.argv[1])
	else:
		exec_tests()


