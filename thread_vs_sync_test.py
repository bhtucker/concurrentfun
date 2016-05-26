# -*- coding: utf-8 -*-
"""
    name
    ~~~~
 
    description
"""
import threading
from functools import reduce


FN = '../loggy'
FAC = 28231

def count_lines(fn):
   print('starting read')
   open(fn, 'r').read()
   print('done reading')
   return

def factorial(n, ix):
   print('factorial {ix} starting'.format(ix=ix)) 
   val = reduce(lambda a, b: a * b, range(1, n, 1))
   print('factorial {ix} done'.format(ix=ix)) 
   return val


def threadtest():
    io_thread = threading.Thread(target=count_lines, args=(FN, ))
    cpu_thread = threading.Thread(target=factorial, args=(FAC, 1))

    io_thread.start()
    cpu_thread.start()

    io_thread.join()
    cpu_thread.join()


def synctest():
    count_lines(FN)
    factorial(FAC, 1)

if __name__ == '__main__':
    from timeit import Timer
    threadtimer = Timer("threadtest()", "from __main__ import threadtest; gc.enable()")
    threadtimer_times = threadtimer.repeat(20, 1)
    synctimer = Timer("synctest()", "from __main__ import synctest; gc.enable()")   
    synctimer_times = synctimer.repeat(20, 1)

    with open('thread_vs_sync_times.csv', 'a') as f:
        for times in zip(threadtimer_times, synctimer_times):
            f.write(','.join(map(str, times))+'\n')
