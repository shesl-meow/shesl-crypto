#!/usr/bin/env python2
# coding=utf-8
from random import randint
from gmpy2 import powmod, gcd

class FactorByED:
    """
    通过 RSA 系统的公钥与私钥，分解 N
    """
    def __init__(self, e, d, n):
        self.e, self.d, self.n = e, d, n
        self.kphi = self.e * self.d - 1

    def factor_by_m(self, m):
        t = self.kphi / 2
        while True:
            pmone = powmod(m, t, self.n)
            p_or_q= gcd(pmone - 1, self.n)
            if p_or_q != 1:
                return p_or_q, self.n / p_or_q
            p_or_q = gcd(pmone + 1, self.n)
            if p_or_q != 1:
                return p_or_q, self.n / p_or_q
            if t%2 == 0: t /= 2
            else: return None

    def factorization(self):
        while True:
            m = randint(0, self.n)
            res = self.factor_by_m(m)
            if res:
                return res if res[0] < res[1] else res[::-1]

if __name__ == "__main__":
    e, d, n = 3, 12, 35
    c = FactorByED(e, d, n)
    print c.factorization()