#!/usr/bin/env python2
#coding=utf-8
from gmpy2 import iroot, is_prime


class FactorNearPQ:
    """
    这个类用于分解两个相近的素数的乘积

    :param n: 两个素数的乘积, RSA 系统的参数
    :return p,q: n 的两个素数因子，前者小于后者
    """
    def __init__(self, n):
        self.n, self.p, self.q = n, 0, 0

    def factor_delta(self):
        k = -1
        while True:
            k += 1
            delta = k ** 2 + 4 * self.n
            res, check = iroot(delta, 2)
            if check: break
        self.p, self.q = (res - k) / 2, (res + k) / 2
        assert is_prime(self.p) and is_prime(self.q)

    def factorization(self):
        self.factor_delta()
        return self.p, self.q

if __name__ == "__main__":
    n = 15
    cnpq = FactorNearPQ(n)
    print(cnpq.factorization())