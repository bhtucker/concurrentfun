import os
import hashlib
from glob import glob
from pyuv_queue import Queue, Full
import pyuv


 
queue = Queue(5)
done = object()
loop = pyuv.Loop()
hash_output = open('hashout', 'w')

def libuv_queue_setup(loop):
    def worker(q):
        for filename in test_setup():
            print(filename)
            fd = open(filename, 'r')
            read_file_to_queue(loop, fd)
        loop.queue_work(lambda: q.put(done), lambda e: e)
    # launch a thread to fetch the items in the background
    loop.queue_work(lambda: worker(queue), lambda e: e)
    # while queue.qsize() > 0:
    #     md5_off_queue(loop, queue)

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

def queue_append_cb(request):
    try:
        queue.put_nowait(request.result)
    except Full:
        md5_off_queue(loop, queue)
        queue_append_cb(request)


def read_file_to_queue(loop, f):
    pyuv.fs.read(loop, f.fileno(), 1024*1000*5, 0, queue_append_cb) 

def md5_off_queue(loop, queue):
    loop.queue_work(lambda: try_hashing(queue.get()), lambda e: e)

def try_hashing(request):
    if not request.result:
        hash_output.write('nothing: %s' % request.error + '\n')
        return
    val = hashlib.md5(request.result).hexdigest()
    return val

def hash_cb(err):
    if err:
        print(err)

def sequential():
    for file in test_setup():
        with open(file, 'r') as f:
            hashlib.md5(f.read()).hexdigest()
    test_cleanup()


def read_and_hash_in_cb(loop):
    descriptors = []
    for file in test_setup():
        f = open(file, 'r')
        pyuv.fs.read(loop, f.fileno(), 1024*1000*5, 0, try_hashing) 
        descriptors.append(f)
    return descriptors

def callback_version():
    descriptors = read_and_hash_in_cb(loop)
    loop.run()
    test_cleanup()

if __name__ == '__main__':
    callback_version()
    # from timeit import Timer
    # sequential_t = Timer("sequential()", "from __main__ import sequential")
    # sequential_times = sequential_t.repeat(50, 1)
    # callback_t = Timer("callback_version()", "from __main__ import callback_version")   
    # callback_times = callback_t.repeat(50, 1)

    # with open('times.csv', 'a') as f:
    #     for times in zip(sequential_times, callback_times):
    #         f.write(','.join(map(str, times))+'\n')
