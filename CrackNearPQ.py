#!/usr/bin/env python2
from gmpy2 import iroot, is_prime


class CrackNearPQ:
    def __init__(self, n):
        self.n, self.p, self.q = n, 0, 0

    def crack_delta(self):
        k = -1
        while True:
            k += 1
            delta = k ** 2 + 4 * self.n
            res, check = iroot(delta, 2)
            if check: break
        self.p, self.q = (res - k) / 2, (res + k) / 2
        assert is_prime(self.p) and is_prime(self.q)

    def crack(self):
        self.crack_delta()
        return self.p, self.q

if __name__ == "__main__":
    n = 15
    cnpq = CrackNearPQ(n)
    print(cnpq.crack())