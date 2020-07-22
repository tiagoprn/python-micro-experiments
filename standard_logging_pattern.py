# coding: utf-8

# TODO: revisit this, does have errors. I have a better example here:
# http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python

# (original reference):
# https://opensourcehacker.com/2016/05/22/python-standard-logging-pattern/

import logging


# This names a logger based on a module so you can switch logger on/off on
# module basis. Although this logging pattern is common, it’s not a universal
# solution. For example if you are creating third party APIs, you might want to
# pass the logger to a class instance of an API,
logger = logging.getLogger(__name__)


class Example(object):
    def __init__(self):
        print('Initialized...')


def my_view(instance):
    # Pass logged objects to logging.Logger.debug() and co. as full and let the
    # logger handle the string formatting. This allows intelligent display of
    # logged objects when using non-console logging solutions like Sentry.
    logger.debug("my_view got request: %s", instance)
    logger.info("my_view got request: %s", instance)
    logger.error("my_view got request: %s and BAD STUFF HAPPENS", instance)

    try:
        raise RuntimeError("OH NOES")
    except Exception as e:
        # Let's log full traceback even when we ignore this exception
        # and it's not risen again
        logger.exception(e)

if __name__ == "__main__":
    instance = Example()
    my_view(instance)
