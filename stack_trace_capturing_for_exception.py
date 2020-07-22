import inspect
import sys
import traceback

'''
This print the full stack trace from the current point in the code
(from where "stack = inspect.stack()", below, is called).

It can be useful, e.g., to understand code that makes many calls
or to get information for debugging exceptions.
'''

# reference:
# https://gist.github.com/diosmosis/1148066


def get_exception_info():
    # this variable is never used. it exists so we can detect if a frame is
    # referencing this specific function.
    __lgw_marker_local__ = 0

    value_to_string = str

    frame_template = '  File "%s", line %i, in %s\n    %s\n'

    log_file = []

    # iterate through the frames in reverse order so we print the
    # most recent frame first
    frames = inspect.getinnerframes(sys.exc_info()[2])
    for frame_info in reversed(frames):
        f_locals = frame_info[0].f_locals

        # if there's a local variable named __lgw_marker_local__, we assume
        # the frame is from a call of this function, 'wrapper', and we skip
        # it. Printing these frames won't help determine the cause of an
        # exception, so skipping it reduces clutter.
        if '__lgw_marker_local__' in f_locals:
            continue

        # log the frame information
        log_file.append(frame_template %
            (frame_info[1], frame_info[2], frame_info[3], frame_info[4][0].lstrip()))

        # log every local variable of the frame
        for k, v in f_locals.items():
            log_file.append('    %s = %s\n' % (k, value_to_string(v)))

        log_file.append('\n')

    return ''.join(log_file)


try:
    print('Hey!')
    raise Exception('forced error!')
except:
    exc_info = get_exception_info()
    print(exc_info)







