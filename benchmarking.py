import sys
import numpy as np 
import time 
import matplotlib.pyplot as plt
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
   
    for j in range(2):
        performance = []
        for n in ns:
            real_counter = np.zeros((n, ch))
            
            if j == 0:
                cs_counter = CountMinSketch(n, ch)
            else:
                cs_counter = CountMedianSketch(n, ch)

            m = 1000000
            start = time.time()
            for i in range(m):
                x = np.clip(int(np.random.normal(n/2, n/7, 1)), 0, n-1)
                c = np.random.normal(1, 3, ch)
                cs_counter.insert(x, np.array(c))
                real_counter[x] += c

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
        