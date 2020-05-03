import pyshark
import numpy as np
import time
import matplotlib.pyplot as plt
from count_min_sketch import CountMinSketch
import sys
from benchmarking import get_size

capture = pyshark.LiveCapture(interface='vEthernet (nat)')

n = 1000  # universe size
ch = 2
real_counter = np.zeros((n, ch))
cs_counter = CountMinSketch(n, ch)

m = 100000
start = time.time()

for packet in capture.sniff_continuously(packet_count=m):

    try:
        x_src = int(int(packet['udp'].srcport) - 5000)
        c_src = np.array([int(packet['ip'].len),0])
        
        x_dst = int(int(packet['udp'].dstport) - 5000)
        c_dst = np.array([0,int(packet['ip'].len)])
        
        cs_counter.insert(x_src, c_src)
        cs_counter.insert(x_dst, c_dst)
        
        real_counter[x_src] += c_src
        real_counter[x_dst] += c_dst
        
        print('-----------------------------')
        print('source: ', x_src)
        print('message size: ', c_src[0])
        print('destination: ', x_dst)

    except (RuntimeError, TypeError, NameError, Exception):
        print("Error Occured")
        pass

        
print(time.time() - start)
print(get_size(cs_counter))

counter = cs_counter.query_all()

plt.grid()
plt.plot(counter[:, 0], 'r-')
plt.plot(real_counter[:, 0], 'b-')
plt.savefig('./result/count_median_sketch_src'+ '.png')
plt.close()

plt.grid()
plt.plot(counter[:, 1], 'r-')
plt.plot(real_counter[:, 1], 'b-')
plt.savefig('./result/count_median_sketch_dst'+ '.png')
plt.close()


