import pytest

from MFPipeline import logs

class testLogs():
    '''
    Class with tests
    '''
    def test_create_log_debug(self):
        log = logs.start_analyst_log("test_debug", "tests/test_logs/", "debug")
        log.debug("Hello! This is debug.")
        log.info("Hello! This is info.")
        log.error("Hello! This is error.")
        logs.close_log(log)

    def test_create_log_info(self):
        log = logs.start_analyst_log("test_info", "tests/test_logs/", "info")
        log.debug("Hello! This is debug.")
        log.info("Hello! This is info.")
        log.error("Hello! This is error.")
        logs.close_log(log)

    def test_create_log_error(self):
        log = logs.start_analyst_log("test_error", "tests/test_logs/", "error")
        log.debug("Hello! This is debug.")
        log.info("Hello! This is info.")
        log.error("Hello! This is error.")
        logs.close_log(log)

def test_run():
    testLogs().test_create_log_debug()
    # testLogs().test_create_log_info()
    # testLogs().test_create_log_error()