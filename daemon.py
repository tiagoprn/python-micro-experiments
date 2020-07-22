"""
This script is a daemon that runs on background.

It writes the current timestamp at a file called '/tmp/testing.txt' at every 3
seconds.

It **requires a 3rd party pypi library named `daemonize`**.

The pid file has the pid of the current execution process. It can be used so as
to prevent simultaneous execution of the script. This also enables monitoring,
so that the script can be (re)started if the pid file is not on the expected
place.
"""
import logging
import os
import sys
from datetime import datetime
from time import sleep

from daemonize import Daemonize

CURRENT_SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]

LOG_FORMAT = (
    '[%(asctime)s PID %(process)s '
    '%(filename)s:%(lineno)s - %(funcName)s()] '
    '%(levelname)s -> \n'
    '%(message)s\n'
)
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
fh = logging.FileHandler(f'/tmp/{CURRENT_SCRIPT_NAME}.log', "a")
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

PIDFILE = f'/tmp/{CURRENT_SCRIPT_NAME}.pid'

DELAY = 3


def main():
    with open('/tmp/testing.txt', 'a') as output_file:
        message = f'NOW: {datetime.now().isoformat()} '
        output_file.write(f'{message}\n')


def loop():
    while True:
        try:
            main()
            logger.info(f'Sleeping for {DELAY} seconds...')
            sleep(DELAY)
        except Exception as e:
            logger.exception('An exception has occurred: {e}')


daemon = Daemonize(
    app=CURRENT_SCRIPT_NAME, pid=PIDFILE, keep_fds=keep_fds, action=loop
)
daemon.start()
