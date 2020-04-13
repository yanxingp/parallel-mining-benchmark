import hashlib
import time
import threading
import multiprocessing

# Difficulty of mining
difficulty = 5
prefix = "0" * difficulty

# Number of trials
ntrial = 10

data = "parallel-mining-benchmark"
global_result = None

def sequential():
    global global_result
    for i in range(ntrial):
        nonce = 0
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
    global found, global_result
    nonce = id
    while not found:
        s = ldata + str(nonce)
        result = hashlib.sha256(s.encode())
        if result.hexdigest()[:5] == prefix:
            global_result = result.hexdigest()
            found = True
        nonce += nthread

def parallel_multi_thread(nthread):
    threads = []
    for i in range(ntrial):
        global found
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
        global found
        found = False
        ldata = data + str(i)
        for i in range(nproc):
            p = multiprocessing.Process(target=mining, args=(i, nproc, ldata))
            procs.append(p)
            p.start()
        
        for t in procs:
            p.join()
    
def main():
    print("-" * 40)
    print("Python Version:")
    print(f"difficulty: {difficulty}, number of trials: {ntrial}")

    # sequential
    print("-" * 40)
    start = time.perf_counter()
    sequential()
    end = time.perf_counter()
    print(f"sequential version:")
    print(f"total time consumed: {end - start:.4f} s")
    print(f"average time consumed: {(end - start) / ntrial:.4f} s")
    print(f"last hash computed: {global_result}")

    # multi-thread parallel
    nthreads = [2, 4, 8, 16]
    for nthread in nthreads:
        print("-" * 40)
        start = time.perf_counter()
        parallel_multi_thread(nthread)
        end = time.perf_counter()
        print(f"{nthread} thread parallel version:")
        print(f"time consumed: {end - start:.4f} s")
        print(f"average time consumed: {(end - start) / ntrial:.4f} s")
        print(f"last hash computed: {global_result}")

    # multi-process parallel
    nprocs = [2, 4, 8, 16]
    for nproc in nprocs:
        print("-" * 40)
        start = time.perf_counter()
        parallel_multi_process(nproc)
        end = time.perf_counter()
        print(f"{nproc} processes parallel version:")
        print(f"time consumed: {end - start:.4f} s")
        print(f"average time consumed: {(end - start) / ntrial:.4f} s")
        print(f"last hash computed: {global_result}")
    print()
    print()

if __name__ == "__main__":
    main()
