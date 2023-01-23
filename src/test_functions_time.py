import time
from functions_math import *

start_time_time = time.time()
# start_time_clock = time.clock()
start_time_perf = time.perf_counter()
start_time_process = time.process_time()

# n = 0
# while n < 10000000:
#     n += 1


n = 0
while n < 10000000:
    # a = -(n + n)
    # if a < 0: a = -a
    # b = n - 2 * n
    # if b < 0: b = -b
    # dist = a + b
    dist_in_taxicab_geometry = abs(-n - n) + abs(n - 2 * n)
    # dist = dist_two_points((n, n), (2*n, 3*n))
    n += 1

print("--- %s seconds (time) ---" % (time.time() - start_time_time))
# print("--- %s seconds (clock) ---" % (time.clock() - start_time_clock))
print("--- %s seconds (perf) ---" % (time.perf_counter() - start_time_perf))
print("--- %s seconds (process) ---" % (time.process_time() - start_time_process))

