# coding: utf-8

# see "bootstraping.py" for a simple decorator that can be reused

try:
    result = 1 / 0
except:
    import traceback
    print 'EXCEPTION: {}'.format(traceback.format_exc(limit=1))
