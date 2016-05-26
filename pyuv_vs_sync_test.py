# -*- coding: utf-8 -*-
"""
    name
    ~~~~
 
    description
"""
import pyuv
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


def pyuv_test():
    loop = pyuv.Loop()
    f = open(FN, 'r')
    pyuv.fs.read(loop, f.fileno(), 1024*1000*590, 0)
    loop.queue_work(lambda: factorial(FAC, 1), lambda e: e)
    loop.run()

def synctest():
    count_lines(FN)
    factorial(FAC, 1)

if __name__ == '__main__':
    from timeit import Timer
    pyuv_test_t = Timer("pyuv_test()", "from __main__ import pyuv_test")
    pyuv_test_t_times = pyuv_test_t.repeat(20, 1)
    synctimer = Timer("synctest()", "from __main__ import synctest")   
    synctimer_times = synctimer.repeat(20, 1)

    with open('pyuv_vs_sync_times.csv', 'a') as f:
        for times in zip(pyuv_test_t_times, synctimer_times):
            f.write(','.join(map(str, times))+'\n')
