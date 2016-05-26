import os
import hashlib
import functools
from glob import glob
from queue import Queue
import threading
 
def async_prefetch_wrapper(iterable, buffer=4):
	"""
	wraps an iterater such that it produces items in the background
	uses a bounded queue to limit memory consumption
	"""
	done = object()
	def worker(q,it):
		for item in it:
			q.put(item)
		q.put(done)
	# launch a thread to fetch the items in the background
	queue = Queue(buffer)
	it = iter(iterable)
	thread = threading.Thread(target=worker, args=(queue, it))
	thread.daemon = True
	thread.start()
	# pull the items of the queue as requested
	while True:
		item = queue.get()
		if item == done:
			return
		else:
			yield item
 
def async_prefetch(func):
	"""
	decorator to make generator functions fetch items in the background
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwds):
		return async_prefetch_wrapper( func(*args, **kwds) )
	return wrapper

def test_setup():
    files = []
    lines = 1000000
    for i in range(10):
        filename = "tempfile%d.txt"%i
        files.append(filename)
        with open(filename, "w") as f:
            f.write(("%s\n" % ','.join([str(i)] * 20) * lines ))
    return files
 
def test_cleanup():
	for f in glob("tempfile*.txt"):
		os.unlink(f)
 
@async_prefetch
def pre_contents(iterable):
	for filename in iterable:
		with open(filename, "rb") as f:
			contents = f.read()
		yield contents
 
def contents(iterable):
	for filename in iterable:
		with open(filename, "rb") as f:
			contents = f.read()
		yield contents

def test(pre=True):
	files = test_setup()
	content_interable = pre_contents(files) if pre else contents(files)
	for c in content_interable:
		hashlib.md5(c).digest()
	test_cleanup()
 
if __name__ == '__main__':
	from timeit import Timer
	no_pre_t = Timer("test(pre=False)", "from __main__ import test; gc.enable()")
	no_pre_times = no_pre_t.repeat(50, 1)
	pre_t = Timer("test(pre=True)", "from __main__ import test; gc.enable()")	
	pre_times = pre_t.repeat(50, 1)

	with open('thread_prefetch_vs_sequential_times.csv', 'a') as f:
		for times in zip(no_pre_times, pre_times):
			f.write(','.join(map(str, times))+'\n')

