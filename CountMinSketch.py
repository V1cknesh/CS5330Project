import random




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

    def update(self, i, c):
        self.N += c
        for j in range(self.d):
            self.C[j][self.hash(j, i)] += c

    def get(self, i):
        e = self.p + 1
        for j in range(self.d):
            e = min(e, self.C[j][self.hash(j, i)])
        return e


