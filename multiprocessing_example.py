# Use the multiprocessing library to distribute the line counting on
# a file across machines/cores.
# According to the original authour, it improves counting a 20 million line
# file from 26 seconds to 7 seconds using an 8 core windows 64 server.
# Note: not using memory mapping makes things much slower.

#  ORIGINAL WORK:
#  http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python

# All credit go to the original writer of this code,
# I have just applied some PEP-8 to it.


import multiprocessing
import sys
import time
import os
import mmap
import logging
import logging.handlers


def init_logger(pid):
    console_format = 'P{0} %(levelname)s %(message)s'.format(pid)
    logger = logging.getLogger()  # New logger at root level
    logger.setLevel(logging.INFO)
    logger.handlers.append(logging.StreamHandler())
    logger.handlers[0].setFormatter(logging.Formatter(
        console_format, '%d/%m/%y %H:%M:%S'))


def get_file_line_count(queues, pid, processes, file1):
    init_logger(pid)
    logging.info('start')

    physical_file = open(file1, "r")
    m1 = mmap.mmap(physical_file.fileno(), 0, None, mmap.ACCESS_READ)

    # work out file size to divide up line counting

    fSize = os.stat(file1).st_size
    chunk = (fSize / processes) + 1

    lines = 0

    # get where I start and stop
    seekStart = chunk * (pid)
    seekEnd = chunk * (pid + 1)
    if seekEnd > fSize:
        seekEnd = fSize

    # find where to start
    if pid > 0:
        m1.seek(seekStart)
        # read next line
        l1 = m1.readline()  # need to use readline with memory mapped files
        seekStart = m1.tell()

    # tell previous rank my seek start to make their seek end

    if pid > 0:
        queues[pid - 1].put(seekStart)
    if pid < processes - 1:
        seekEnd = queues[pid].get()

    m1.seek(seekStart)
    l1 = m1.readline()

    while len(l1) > 0:
        lines += 1
        l1 = m1.readline()
        if m1.tell() > seekEnd or len(l1) == 0:
            break

    logging.info('done')
    #  add up the results
    if pid == 0:
        for p in range(1, processes):
            lines += queues[0].get()
        queues[0].put(lines)  # the total lines counted
    else:
        queues[0].put(lines)

    m1.close()
    physical_file.close()


if __name__ == '__main__':
    init_logger('main')
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        logging.fatal('parameters required: file-name [processes]')
        exit()

    t = time.time()
    processes = multiprocessing.cpu_count()
    if len(sys.argv) > 2:
        processes = int(sys.argv[2])
    queues = []  # a queue for each process
    for pid in range(processes):
        queues.append(multiprocessing.Queue())
    jobs = []
    prev_pipe = 0
    for pid in range(processes):
        p = multiprocessing.Process(target=get_file_line_count,
                                    args=(queues, pid, processes, file_name,))
        p.start()
        jobs.append(p)

    jobs[0].join()  # wait for counting to finish
    lines = queues[0].get()

    logging.info('finished {} Lines:{}'.format(time.time() - t, lines))
