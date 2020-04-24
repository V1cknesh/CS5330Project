import random
from memory_profiler import profile



class CountMinSketch(object):

    def __init__(self, w, d, p):
        self.w = w
        self.d = d
        self.p = p
        self.C = [[0] * self.w for _ in range(self.d)]
        self.a = [random.randint(1, self.p) for _ in range(self.d)]
        self.b = [random.randint(1, self.p) for _ in range(self.d)]
        self.N = 0


    def hash(self, j, i):
        return (self.a[j] * i + self.b[j] % self.p) % self.w


    @profile
    def update(self, i, c):
        self.N += c
        for j in range(self.d):
            self.C[j][self.hash(j, i)] += c

    @profile
    def remove(self, i, c):
        self.N -= c
        for j in range(self.d):
            self.C[j][self.hash(j, i)] -= c

    @profile
    def get(self, i):
        e = self.p + 1
        for j in range(self.d):
            e = min(e, self.C[j][self.hash(j, i)])
        return e


def sentimentToInteger(floating_point_number):

    width = 1000

    epsilon = 2 / width

    start = -1

    for i in range(1, width + 1):
        if ( floating_point_number > start and floating_point_number <= start + epsilon):
            return i
        else:
            start  += epsilon


if __name__ == '__main__':

    file = open("sentiment.txt", "r")
    sketch = CountMinSketch(2000, 10, 2 ** 31 - 1)

    f1 = file.readlines()
    for score in f1:
        sketch.update(sentimentToInteger(float(score)), 1)
        

    print(sketch.get(500))













