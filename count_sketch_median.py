import numpy as np 
import matplotlib.pyplot as plt
import time 

class CountMedianSketch:

    def __init__(self, n, ch = 1, epsilon=0.1, delta = 0.01):
        self.n = n
        self.ch = ch
        self.w = int(3./epsilon**2) #bucket size
        self.d = int(20*np.log(1./delta))        
        self.p = self.get_nearest_prime(self.w)    

        self.hash_params = np.random.randint(0, self.p, (self.d, 2))
        self.signs_params = np.random.randint(0, 2, self.d)

        self.c_table = np.zeros((self.d, self.w, ch))
        self.arange_ind = np.arange(self.c_table.shape[0], dtype=np.int32)

    def query_all(self):
        counter = np.zeros((self.n, self.ch))
        for i in range(self.n):
            counter[i] = self.query(i)
        return counter

    def query(self, x):
        #query one item
        ind = self.get_hash_ind(x)
        sign = self.get_sign(x)
        min_val = np.median(np.multiply(sign[:, np.newaxis],self.c_table[self.arange_ind, ind]), axis = 0)
        return min_val

    def insert(self, x, c):
        ind = self.get_hash_ind(x)
        sign = self.get_sign(x)
        self.c_table[self.arange_ind, ind] += sign[:, np.newaxis].dot(c[np.newaxis, :])

    def get_sign(self, x):
        ind = np.mod(x+self.signs_params, 2)*2-1
        return ind

    def get_hash_ind(self, x):
        ind = np.mod(np.mod((self.hash_params[:, 0]*x+self.hash_params[:, 1]), self.p), self.w)
        return ind

    def sieve(self, n):
        mask = np.ones(n+1)
        mask[:2] = 0
        for i in range(2, int(n**.5)+1):
            if not mask[i]:
                continue
            mask[i*i::i] = 0
        return np.argwhere(mask)

    def get_nearest_prime(self, old_number):
        try:
            n = np.max(self.sieve(2*old_number-1))
            if n < old_number+1: return None
            return n
        except ValueError:
            return None

if __name__ == '__main__':
    #CountSketch
    #tradeoff between k and epsilon to get optimum speed and memory

    n = 50  #universe size
    ch = 3

    real_counter = np.zeros((n,ch))
    cs_counter = CountMedianSketch(n, ch)

    start = time.time()

    m = 30000
    for i in range(m):
        x = np.clip(int(np.random.normal(16, 7, 1)), 0, n-1)
        c = np.random.normal(1,2,ch)        
        cs_counter.insert(x, c)
        real_counter[x] += c

    print(time.time()-start)

    counter = cs_counter.query_all()
    # error = epsilon*np.sqrt(np.sum(np.square(real_counter)))
    # success_rate = float(np.sum(np.absolute(counter-real_counter)<error))/(n*ch)
    # print(success_rate)

    plt.plot(counter, 'r-')
    plt.plot(real_counter, 'b-')
    plt.show()