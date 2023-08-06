# coding:utf-8
import subprocess
import pytest

from apiTestMain import FILE_PATH, ENV_NAME, TEST_CASES
from apitestbasiclib.apitestlogic import apitest
def runApiCases():
    print('runCases run ......')
    subprocess.call('pytest testCasesRun.py',shell=False)
print('_FILE_PATH=%s,_ENV_NAME=%s'% (FILE_PATH,ENV_NAME))
print('_TEST_CASES=%s' % TEST_CASES)
@pytest.mark.parametrize('test_cases',TEST_CASES)
def test_http_request(test_cases):
    print('test_yamlapi run ......')
    apitest(test_cases,ENV_NAME)
