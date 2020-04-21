import numpy as np 
import matplotlib.pyplot as plt
import time 


class CountMinSketch:

    def __init__(self, n, epsilon = 0.1, delta = 0.01):
        w = int(np.e/epsilon) #bucket size
        d = 1 + int(np.log(1./delta)) #no of hash

        self.n = n
        self.hash_functions_params = []
        for i in range(d):
            p = self.get_nearest_prime(w)
            a = np.random.randint(0, p)
            b = np.random.randint(0, p)
            self.hash_functions_params.append([w, p, a, b])
            self.c_table = np.zeros((d, w))

        #store hash table
        self.hash_table = np.zeros((n, d), dtype=np.int32)
        for i in range(n):
            for j in range(d):
                ind = self.hash(i, self.hash_functions_params[j])
                self.hash_table[i, j] = ind
        self.arange_ind = np.arange(self.c_table.shape[0], dtype=np.int32)

    def get_counter(self):
        #query all items
        counter = np.zeros(self.n)
        for i in range(self.n):
            counter[i] = self.query(i)
        return counter

    def query(self, x):
        #query one item
        min_val = np.amin(self.c_table[self.arange_ind, self.hash_table[x]])
        return min_val

    def insert(self, x, c):
        self.c_table[self.arange_ind, self.hash_table[x]] += c

    def hash(self, x, param):
        w, p, a, b = param
        return ((a*x+b)%p)%w

    def get_nearest_prime(self, old_number):
        try:
            n = np.max(self.seive(2*old_number-1))
            if n < old_number+1: return None
            return n
        except ValueError:
            return None

    def seive(self, n):
        mask = np.ones(n+1)
        mask[:2] = 0
        for i in range(2, int(n**.5)+1):
            if not mask[i]:
                continue
            mask[i*i::i] = 0
        return np.argwhere(mask)

n = 50  #universe size
epsilon = 0.1
real_counter = np.zeros(n)
cs_counter = CountMinSketch(n, epsilon)

m = 30000
start = time.time()
for i in range(m):
    x = np.clip(int(np.random.normal(25, 7, 1)), 0, n-1)
    c = int(np.random.normal(1, 3, 1))
    
    cs_counter.insert(x, c)
    real_counter[x] += c


#without query 0.45s for 30k 
#with query 6.32s for 30k

print(time.time()-start)

counter = cs_counter.get_counter()

error = epsilon*m
success_rate = float(np.sum(np.absolute(counter-real_counter)<error))/n

print(success_rate)

plt.plot(counter, 'r-')
plt.plot(real_counter, 'b-')
plt.show()
