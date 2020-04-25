import numpy as np 
import matplotlib.pyplot as plt
import time 

class SimpleCountSketch:

    def __init__(self, n, ch, epsilon=0.01):
        self.n = n
        self.ch = ch
        w = int(3./epsilon**2) #bucket size
        p = self.get_nearest_prime(w)
        a = np.random.randint(0, p)
        b = np.random.randint(0, p)
        self.param = [w, p, a, b]
        self.signs = np.ones(n)
        self.signs[np.random.sample([n]) < 0.5] = -1
        self.c_table = np.zeros((w, ch))

    def query_all(self):
        counter = np.zeros((self.n, self.ch))
        for i in range(self.n):
            counter[i] = self.query(i)
        return counter

    def query(self, x):
        ind = self.hash(x, self.param)
        return self.signs[x]*self.c_table[ind]

    def insert(self, x, c):
        ind = self.hash(x, self.param)
        self.c_table[ind] += self.signs[x]*c

    def hash(self, x, param):
        w, p, a, b = param
        return ((a*x+b)%p)%w

    def seive(self, n):
        mask = np.ones(n+1)
        mask[:2] = 0
        for i in range(2, int(n**.5)+1):
            if not mask[i]:
                continue
            mask[i*i::i] = 0
        return np.argwhere(mask)

    def get_nearest_prime(self, old_number):
        try:
            n = np.max(self.seive(2*old_number-1))
            if n < old_number+1: return None
            return n
        except ValueError:
            return None

class CountMedianSketch:

    def __init__(self, n, ch, d, epsilon=0.01):
        self.n = n
        self.ch = ch
        w = int(3./epsilon**2) #bucket size

        self.signs = np.ones(n)
        self.signs[np.random.sample([n]) < 0.5] = -1

        self.hash_functions_params = []
        for i in range(d):
            p = self.get_nearest_prime(w)
            a = np.random.randint(0, p)
            b = np.random.randint(0, p)
            self.hash_functions_params.append([w, p, a, b])

        self.c_table = np.zeros((d, w, ch))

        self.hash_table = np.zeros((n, d), dtype=np.int32)
        for i in range(n):
            for j in range(d):
                ind = self.hash(i, self.hash_functions_params[j])
                self.hash_table[i, j] = ind
        self.arange_ind = np.arange(self.c_table.shape[0], dtype=np.int32)

    def query_all(self):
        counter = np.zeros((self.n, self.ch))
        for i in range(self.n):
            counter[i] = self.query(i)
        return counter

    def query(self, x):
        #query one item
        min_val = np.median(self.signs[x]*self.c_table[self.arange_ind, self.hash_table[x]], axis = 0)
        return min_val

    def insert(self, x, c):
        self.c_table[self.arange_ind, self.hash_table[x]] += self.signs[x]*c

    def hash(self, x, param):
        w, p, a, b = param
        return ((a*x+b)%p)%w

    def seive(self, n):
        mask = np.ones(n+1)
        mask[:2] = 0
        for i in range(2, int(n**.5)+1):
            if not mask[i]:
                continue
            mask[i*i::i] = 0
        return np.argwhere(mask)

    def get_nearest_prime(self, old_number):
        try:
            n = np.max(self.seive(2*old_number-1))
            if n < old_number+1: return None
            return n
        except ValueError:
            return None



if __name__ == '__main__':
    #CountSketch
    #tradeoff between k and epsilon to get optimum speed and memory

    n = 50  #universe size
    d = 8
    epsilon = 0.1
    ch = 2

    real_counter = np.zeros((n,ch))
    cs_counter = CountMedianSketch(n, ch, d, epsilon)

    start = time.time()

    m = 30000
    for i in range(m):
        x = np.clip(int(np.random.normal(16, 7, 1)), 0, n-1)
        c = np.random.normal(1,2,ch)
        
        cs_counter.insert(x, c)
        real_counter[x] += c

    #0.58s for 30k
    print(time.time()-start)

    counter = cs_counter.query_all()
    error = epsilon*np.sqrt(np.sum(np.square(real_counter)))
    success_rate = float(np.sum(np.absolute(counter-real_counter)<error))/(n*ch)

    print(success_rate)

    plt.plot(counter, 'r-')
    plt.plot(real_counter, 'b-')
    plt.show()