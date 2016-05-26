# -*- coding: utf-8 -*-
"""
    name
    ~~~~
 
    description
"""
import asyncio
from functools import reduce

FN = '/Users/bhtucker/chatid/citadel/log-service-event-log-2015-09-13-1800'

def count_lines(fn):
   # out = []
   print('starting read')
   val = open(fn, 'r').read()
   print('done reading')
   # with open(fn, 'r') as f:
   #    out = f.readlines()
   return val

def factorial(n, ix):
   print('factorial {ix} starting'.format(ix=ix)) 
   val = reduce(lambda a, b: a * b, range(1, n, 1))
   print('factorial {ix} done'.format(ix=ix)) 
   return val

@asyncio.coroutine
def print_data_size(do_factorial=True):
   data = yield from get_data_size(do_factorial=do_factorial)
   print("Stuff: {}".format(data)[:40])


if __name__ == '__main__':
    @asyncio.coroutine
    def get_data_size(do_factorial=True):
        loop = asyncio.get_event_loop()

        # These each run in their own thread (in parallel)
        future1 = loop.run_in_executor(None, count_lines, FN)
        if do_factorial:
            future2 = loop.run_in_executor(None, factorial, 18231, 1) # 32300
        # loop.run_in_executor(None, factorial, 32300, 2)

        # While the synchronous code above is running in other threads, the event loop
        # can go do other things.
        data1 = yield from future1
        if do_factorial:
            data2 = yield from future2
        else:
            data2 = None
        return len(data1), data2

    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_data_size(do_factorial=True))
