import hashlib
import time
import threading
import multiprocessing

# Difficulty of mining
difficulty = 5
prefix = "0" * difficulty

# Number of trials
ntrial = 5

data = "parallel-mining-benchmark"
global_result = None

def sequential():
    nonce = 0
    global global_result
    for i in range(ntrial):
        ldata = data + str(i)
        while True:
            s = ldata + str(nonce)
            result = hashlib.sha256(s.encode())
            if result.hexdigest()[:5] == prefix:
                # print(result.hexdigest())
                global_result = result.hexdigest()
                break
            nonce += 1

# Use shared memory for inter-thread communication.
# Ignore race conditions handling, 
# because it is essentially a 'race' between the thread
found = False
def mining(id, nthread, ldata):
    global found
    nonce = id
    while not found:
        s = ldata + str(nonce)
        result = hashlib.sha256(s.encode())
        if result.hexdigest()[:5] == prefix:
            global_result = result.hexdigest()
            break
        nonce += nthread

def parallel_multi_thread(nthread):
    threads = []
    for i in range(ntrial):
        found = False
        ldata = data + str(i)
        for i in range(nthread):
            t = threading.Thread(target=mining, args=(i, nthread, ldata))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()

def parallel_multi_process(nproc):
    procs = []
    for i in range(ntrial):
        found = False
        ldata = data + str(i)
        for i in range(nproc):
            p = multiprocessing.Process(target=mining, args=(i, nproc, ldata))
            procs.append(p)
            p.start()
        
        for t in procs:
            p.join()
    
def main():
    print(f"difficult: {difficulty}, number of trials: {ntrial}")

    # sequential
    print("-" * 40)
    start = time.perf_counter()
    sequential()
    end = time.perf_counter()
    print(f"sequential version:")
    print(f"total time consumed: {end - start}")
    print(f"average time consumed: {(end - start) / ntrial}")
    print(f"last hash computed: {global_result}")

    # # multi-thread parallel
    print("-" * 40)
    nthread = 4
    start = time.perf_counter()
    parallel_multi_thread(nthread)
    end = time.perf_counter()
    print(f"{nthread} thread parallel version:")
    print(f"time consumed: {end - start}")
    print(f"average time consumed: {(end - start) / ntrial}")
    print(f"last hash computed: {global_result}")

    # multi-process parallel
    print("-" * 40)
    nproc = 8
    start = time.perf_counter()
    parallel_multi_process(nproc)
    end = time.perf_counter()
    print(f"{nproc} processes parallel version:")
    print(f"time consumed: {end - start}")
    print(f"average time consumed: {(end - start) / ntrial}")
    print(f"last hash computed: {global_result}")

if __name__ == "__main__":
    main()
