import pyshark
import numpy as np
import time
import matplotlib.pyplot as plt
from count_min_sketch import CountMinSketch
import sys

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size



capture = pyshark.LiveCapture(interface='vEthernet (nat)')

#Count Min Sketch


n = 50  # universe size
ch = 2
real_counter = np.zeros((n, ch))
cs_counter = CountMinSketch(n, ch)

m = 10000000
mi = 0
start = time.time()

for packet in capture.sniff_continuously(packet_count=None):
    mi += 1
    if (mi <= m):
        try:
            x = int(packet['udp'].srcport)
            c = int(packet['ip'].len)
            cs_counter.insert(x, np.array(c))
            cs_counter.insert(x, np.array(c))
            real_counter[x] += c
            print(mi)

        except (RuntimeError, TypeError, NameError, Exception):
            pass
    else:
        break
        
print(time.time() - start)
#print(get_size(cs_counter))

counter = cs_counter.query_all()

plt.grid()
plt.plot(counter, 'r-')
plt.plot(real_counter, 'b-')
plt.savefig('./result/count_min_sketch'+ '.png')
plt.close()





