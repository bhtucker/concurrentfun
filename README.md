# concurrentfun
Scripts attempting to efficiently schedule disk io and cpu in one process


![Release it!](releasethegil.png)


# Threading vs the GIL

Can we beat the performance of sequential code?

### Factorial Task
![Factorial](thread_vs_sync.png)

### MD5s Task
![MD5](thread_prefetch_vs_sync.png)



# Without using stdlib io module?

Can use `libuv`, the cross platform asynchronous IO library that backs, among other things, node.js

### Factorial Task
![Factorial](pyuv_vs_seq.png)

### MD5s Task

![MD5s](cb_vs_sync.png)

