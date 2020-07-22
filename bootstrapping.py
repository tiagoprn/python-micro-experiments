import functools
import logging
import os
import sys
import traceback

CURRENT_SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
LOG_FORMAT = ('[%(asctime)s PID %(process)s '
              '%(filename)s:%(lineno)s - %(funcName)s()] '
              '%(levelname)s -> \n'
              '%(message)s\n')
# Configure the logging both to file and to console. Works from python 3.3+
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    handlers=[
        logging.FileHandler(f'{CURRENT_SCRIPT_NAME}.log'),
        logging.StreamHandler(sys.stdout)
    ])

def catch_exceptions(func):
    '''
    A decorator to automatically catch exceptions. Can be extended to use,
    e.g., sentry/raven to provide a context and more detailed traceback info.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            logging.error(f'Exception ocurred: {traceback.format_exc()}, context={locals()}')
    return wrapper


class Worker(object):
    def __init__(self, param1):
        self.__private_var = ""
        self.param1 = param1

    @catch_exceptions
    def run(self):
        logging.info(f"The value of param1 is: '{self.param1}'")
        logging.info(f"I ran. Woohoo!")
        raise Exception('Forcing an exception here to test the decorator.')

if __name__ == "__main__":
    worker = Worker(param1=12.76523)
    worker.run()

