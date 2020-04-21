
class SimpleCountSketch:

    def __init__(self, n, w):
        self.n = n
        p = self.get_nearest_prime(w)
        a = np.random.randint(0, p)
        b = np.random.randint(0, p)
        self.param = [w, p, a, b]
        self.signs = np.ones(n)
        self.signs[np.random.sample([n]) < 0.5] = -1
        self.c_table = np.zeros(w)

    def get_counter(self):
        counter = np.zeros(self.n)
        for i in range(self.n):
            counter[i] = self.query(i)
        return counter

    def query(self, x):
        ind = self.hash(x, self.param)
        return self.signs[x]*self.c_table[ind]

    def insert(self, x):
        ind = self.hash(x, self.param)
        self.c_table[ind] += self.signs[x]

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

class MedianCountSketch:
    cs_counters = []

    def __init__(self, k, n, w):
        #create k separate count sketches
        for i in range(k):
            self.cs_counters.append(SimpleCountSketch(n, w))

    def insert(self, x):
        for i in range(k):
            self.cs_counters[i].insert(x)

    def get_counter(self):
        res = []
        for i in range(k):
            res.append(self.cs_counters[i].get_counter())

        return np.median(res, axis = 0)


#CountSketch

# n = 50  #universe size
# epsilon = 0.01
# w = int(3./epsilon**2) #bucket size
# k = 8

# real_counter = np.zeros(n)
# cs_counter = MedianCountSketch(k, n, w)

# start = time.time()
# m = 30000
# for i in range(m):
#     x = np.clip(int(np.random.normal(16, 7, 1)), 0, n-1)
#     real_counter[x] += 1
#     cs_counter.insert(x)

# #0.58s for 30k

# print(time.time()-start)

# counter = cs_counter.get_counter()
# error = epsilon*np.sqrt(np.sum(np.square(real_counter)))
# success_rate = float(np.sum(np.absolute(counter-real_counter)<error))/n

# print(counter)
# print(real_counter)

# plt.plot(counter)
# plt.plot(real_counter)
# plt.show()

# print(n, w)
# print(error)
# print(success_rate)