#!/usr/bin/env python3

"""
Context managers can be used when you want to avoid repetitive code,
that should do the same thing from times to times.
"""

from time import sleep
import logging

from contextlib import contextmanager, ContextDecorator
from datetime import datetime

@contextmanager
def timing(description: str) -> None:
    start = datetime.now()
    yield  # this is where the decorated or contextualized code will do its job.
    elapsed_seconds = (datetime.now() - start).seconds
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time= '{:02}h:{:02}m:{:02}s'.format(
        int(hours), int(minutes), int(seconds))
    print(f"[timing report] '{description}' "
          f"took {elapsed_time}")


class SuccessfulCounter(ContextDecorator):
    def __init__(self, description):
        self.description = description
        self.error= 0
        self.success = 0
        self.start = None
        self.successful = None

    def __enter__(self, *args):
        self.start = datetime.now()
        return self

    def __exit__(self, type, value, traceback):
        elapsed_seconds = (datetime.now() - self.start).seconds
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time= '{:02}h:{:02}m:{:02}s'.format(
            int(hours), int(minutes), int(seconds))
        print(f"[timing report] '{self.description}' "
            f"took {elapsed_time}")

        if type:  # That means an exception was raised
            self.error += 1
        else:
            self.success += 1

        self.successful = not self.error

        print(f'ERROR count = {self.error}, SUCCESS count = {self.success}')


@timing('do some work')  # here I use the context manager as a decorator
def do_work():
    with timing('Sleep for 1 second'):  # here I use the context manager with the with clause
        sleep(1)

    with timing('Print characters on your screen.'):  # still using the with clause
        print('-' * 1000)

    print('-' * 80)

    with SuccessfulCounter('Divide a value for 2') as counter:
        result = 4 / 2
        print(f'4/2 = {result}')
    print(f'Counter status: errors={counter.error}, '
          f'successes={counter.success}')
    print('-' * 80)

do_work()

print('Successfully finished.')
