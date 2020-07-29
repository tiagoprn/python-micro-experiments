#!/usr/bin/env python3

"""
Context managers can be used when you want to avoid repetitive code,
that should do the same thing from times to times.
"""
import logging
import os
import tracemalloc
from contextlib import ContextDecorator, contextmanager
from datetime import datetime
from time import sleep


@contextmanager
def timing(description: str) -> None:
    start = datetime.now()
    yield  # this is where the decorated or contextualized code will do its job.
    elapsed_seconds = (datetime.now() - start).seconds
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time = '{:02}h:{:02}m:{:02}s'.format(
        int(hours), int(minutes), int(seconds)
    )
    print(f"[timing report] '{description}' " f"took {elapsed_time}")


class SimpleProfiler(ContextDecorator):
    """
    A simple profiler to track memory usage. Based on work from:

    https://medium.com/survata-engineering-blog/monitoring-memory-usage-of-a-running-python-program-49f027e3d1ba
    """

    def __init__(self, path: str = '/tmp/profiler.csv'):
        self.path = path
        self.current = 0
        self.peak = 0
        if not os.path.exists(self.path):
            with open(self.path, 'a') as output_file:
                output_file.write(
                    f'timestamp, file, function, current_memory_in_mb, '
                    f'peak_memory_in_mb\n'
                )

    def __enter__(self, *args):
        tracemalloc.start()
        self.snapshot()

    def snapshot(self):
        self.current, self.peak = tracemalloc.get_traced_memory()
        with open(self.path, 'a') as output_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            filename = os.path.basename(__file__)
            measured = (
                f'{timestamp}, {filename}, {__name__},  '
                f'{self.current / 10**6}, {self.peak / 10**6}\n'
            )
            output_file.write(measured)
            tracemalloc.stop()

    def __exit__(self, *args):
        self.snapshot()


class SuccessfulCounter(ContextDecorator):
    def __init__(self, description):
        self.description = description
        self.error = 0
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
        elapsed_time = '{:02}h:{:02}m:{:02}s'.format(
            int(hours), int(minutes), int(seconds)
        )
        print(f"[timing report] '{self.description}' " f"took {elapsed_time}")

        if type:  # That means an exception was raised
            self.error += 1
        else:
            self.success += 1

        self.successful = not self.error

        print(f'ERROR count = {self.error}, SUCCESS count = {self.success}')


def test_profiler():
    with SimpleProfiler():
        print('Doing #1')

    with SimpleProfiler():
        print('Doing #2')

    with SimpleProfiler():
        print('Doing #3')


@timing('do some work')  # here I use the context manager as a decorator
def do_work():
    with timing(
        'Sleep for 1 second'
    ):  # here I use the context manager with the with clause
        sleep(1)

    with timing(
        'Print characters on your screen.'
    ):  # still using the with clause
        print('-' * 1000)

    print('-' * 80)

    with SuccessfulCounter('Divide a value for 2') as counter:
        result = 4 / 2
        print(f'4/2 = {result}')
    print(
        f'Counter status: errors={counter.error}, '
        f'successes={counter.success}'
    )
    print('-' * 80)


do_work()
test_profiler()
print('Successfully finished.')
