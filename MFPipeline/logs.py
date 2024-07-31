import logging

import os
import sys

def start_analyst_log(event_name, log_location, log_type, stream=False):
    '''
    Function that creates logs for analysts.
    :param event_name: name of event assigned to the analyst
    :param log_location: str, location of the log.
    :param log_type: str, which level of logging to initialize.
    :param stream: optional, boolean, should the log be accessible through Kubernetes?

    :return: python logger
    '''

    log = logging.getLogger('analyst_log')

    if (log_type == 'debug'):
        log_level = logging.DEBUG
    elif (log_type == 'info'):
        log_level = logging.INFO
    else:
        log_level = logging.ERROR

    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    log.setLevel(log_level)

    if (stream):
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        log.addHandler(ch)
    else:
        filename = log_location + '%s_analyst.log' % event_name
        fh = logging.FileHandler(filename, encoding='utf-8')
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    log.info("Processing started. Opened log.")
        
    return log


def close_log(log):
    '''
    Function that closes a log.

    :param log: log to close
    '''

    for handler in log.handlers:
        log.info('Processing complete.\n')
        if isinstance(handler, logging.FileHandler):
            handler.close()
        log.removeFilter(handler)
