import sys
import numpy as np 
import time 
import matplotlib.pyplot as plt
import pyshark
from count_min_sketch import CountMinSketch
from count_sketch_median import CountMedianSketch

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

if __name__ == '__main__':

    #find speed, memory usage, and 
    ns = [10, 30, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    ch = 1
    capture = pyshark.LiveCapture(interface='vEthernet (nat)')

   
    for j in range(2):
        performance = []
        for n in ns:
            real_counter = np.zeros((n, ch))
            
            if j == 0:
                cs_counter = CountMinSketch(n, ch)
            else:
                cs_counter = CountMedianSketch(n, ch)

            m = 1000000
            mi = 0
            start = time.time()
            for packet in capture.sniff_continuously(packet_count=None):
                if (mi < m):
                    try:
                        x = int(packet['udp'].srcport)
                        print(x)
                        print(mi)
                        c = 1
                        cs_counter.insert(x, np.array(c))
                        real_counter[x] += c
                        mi += 1
                    except (RuntimeError, TypeError, NameError, Exception):
                        mi += 1
                        pass
                else:
                    break

            total_time = (time.time()-start)/m
            counter = cs_counter.query_all()
            norm_rmse = np.sqrt(np.sum(np.mean(np.square(counter-real_counter))))/(float(m)/n)
            memory = get_size(cs_counter)

            # print(sys.getsizeof(cs_counter.c_table))

            # print(sys.getsizeof(cs_counter.hash_params))

            #time in s, memory in bytes
            res = [n, total_time, norm_rmse, memory]
            performance.append(res)
            print(res)
            plt.grid()
            plt.plot(counter, 'r-')
            plt.plot(real_counter, 'b-')
            plt.savefig('./result/benchmark_'+str(j)+'_'+str(n)+'.png')
            plt.close()
        
        performance = np.asarray(performance)
        np.savetxt('./result/benchmark_'+str(j)+'.csv', performance, delimiter=',')

    n = 500
    epsilons = [0.001, 0.01, 0.1, 0.2, 0.5]
    performance = []
    for epsilon in epsilons:
        real_counter = np.zeros((n, ch))
        
        cs_counter = CountMedianSketch(n, ch, epsilon = epsilon)

        m = 1000000
        mi = 0
        start = time.time()
        for packet in capture.sniff_continuously(packet_count=None):
            if (mi < m):
                try:
                    x = int(packet['udp'].srcport)
                    print(x)
                    print(mi)
                    c = 1
                    cs_counter.insert(x, np.array(c))
                    real_counter[x] += c
                    mi += 1
                except (RuntimeError, TypeError, NameError, Exception):
                    mi += 1
                    pass
            else:
                break

        total_time = (time.time()-start)/m
        counter = cs_counter.query_all()
        norm_rmse = np.sqrt(np.sum(np.mean(np.square(counter-real_counter))))/(float(m)/n)
        memory = get_size(cs_counter)

        #time in s, memory in bytes
        res = [epsilon, total_time, norm_rmse, memory]
        performance.append(res)
        print(res)
        plt.grid()
        plt.plot(counter, 'r-')
        plt.plot(real_counter, 'b-')
        plt.savefig('./result/benchmark_2_'+str(epsilon)+'.png')
        plt.close()
    
    performance = np.asarray(performance)
    np.savetxt('./result/benchmark_2.csv', performance, delimiter=',')

    
    n = 500
    deltas = [0.001, 0.01, 0.1, 0.2, 0.5]
    performance = []
    for delta in deltas:
        real_counter = np.zeros((n, ch))
        
        cs_counter = CountMedianSketch(n, ch, delta = delta)

        m = 1000000
        mi = 0
        start = time.time()
        for packet in capture.sniff_continuously(packet_count=None):
            if (mi < m):
                try:
                    x = int(packet['udp'].srcport)
                    print(mi)
                    c = 1
                    cs_counter.insert(x, np.array(c))
                    real_counter[x] += c
                    mi += 1
                except (RuntimeError, TypeError, NameError, Exception):
                    mi += 1
                    pass
            else:
                break

        total_time = (time.time()-start)/m
        counter = cs_counter.query_all()
        norm_rmse = np.sqrt(np.sum(np.mean(np.square(counter-real_counter))))/(float(m)/n)
        memory = get_size(cs_counter)

        #time in s, memory in bytes
        res = [delta, total_time, norm_rmse, memory]
        performance.append(res)
        print(res)
        plt.grid()
        plt.plot(counter, 'r-')
        plt.plot(real_counter, 'b-')
        plt.savefig('./result/benchmark_3_'+str(delta)+'.png')
        plt.close()
    
    performance = np.asarray(performance)
    np.savetxt('./result/benchmark_3.csv', performance, delimiter=',')
