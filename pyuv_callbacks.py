import os
import hashlib
from glob import glob
import pyuv
 
loop = pyuv.Loop()


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

def try_hashing(request):
    if not request.result:
        print('nothing: %s' % request.error + '\n')
        return
    val = hashlib.md5(request.result).hexdigest()
    return val


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
    from timeit import Timer
    sequential_t = Timer("sequential()", "from __main__ import sequential")
    sequential_times = sequential_t.repeat(50, 1)
    callback_t = Timer("callback_version()", "from __main__ import callback_version")   
    callback_times = callback_t.repeat(50, 1)

    with open('times.csv', 'a') as f:
        for times in zip(sequential_times, callback_times):
            f.write(','.join(map(str, times))+'\n')
