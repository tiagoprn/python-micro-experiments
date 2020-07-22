# coding: utf-8
"""
MOTIVATION:
    Your script motivation here

HOW THIS WORKS:
    1) Step 1
    2) Step 2
    3) Step 3

IMPLEMENTATION NOTES:
    * Requires the python lib "newspaper":
        $ pip install newspaper
"""

import sys
import traceback
import logging

# Constants section
DEBUG_MODE = True

# Sets up the logging
logging.basicConfig(filename="log.txt",
                    format="[%(asctime)s - PID %(process)s - %(module)s.py - %(levelname)s] %(message)s",
                    filemode='w',  # or 'a' to keep appending the file forever
                    level=logging.DEBUG if DEBUG_MODE else logging.ERROR)


def get_exception_full_stacktrace(e):
    trace = traceback.format_tb(sys.exc_info()[2])
    unicode_trace = []
    for elem in trace:
        unicode_trace.append(elem.decode('utf8'))
        trace_str = u'\n'.join(unicode_trace)
        excecao = u'EXCEPTION: "%s"\t- EXCEPTION TYPE: "%s"\t- TRACEBACK:\t%s' % (
            e, type(e), trace_str)
        unicode_trace.append(excecao)
    return '\n'.join(unicode_trace)


class Worker(object):
    def run(self):
        logging.debug("run() - [WAIT]")
        from newspaper import Article

        '''
        Library documentation: http://newspaper.readthedocs.org/en/latest/user_guide/quickstart.htm
        '''

        NOTES_LIST = [
            '118',
            '117',
            # '116',
            # '115',
        ]
        for note_id in NOTES_LIST:
            note = Article(url="http://site.tiagoprnl.in/core/visitor_home/nota/%s/" % note_id)
            note.download()

            print '*' * 100
            # print 'H T M L'
            # print note.html
            #print '*' * 100
            # print 'T E X T'
            note.parse()
            print note.text


        logging.debug("run() - [DONE]")

if __name__ == "__main__":
    try:
        worker = Worker()
        worker.run()
        raise Exception(u"Forcing an exception to be logged.")
    except Exception, e:
        logging.error(get_exception_full_stacktrace(e))
