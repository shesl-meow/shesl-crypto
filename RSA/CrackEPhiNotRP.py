#!/usr/bin/env python2
#coding=utf-8
from sage.all import crt, inverse_mod, Integer
from gmpy2 import is_prime, powmod, gcd
from CrackSmallE import CrackSmallE


class CrackEPhiNotRP:
    """
    这个类用于 RSA 系统中 n 的欧拉函数跟指数 e 不互素时来解明文

    :param c: RSA 系统的密文
    :param e: RSA 系统的指数
    :param p,q: RSA 系统的两个素数

    :return m: 调用任何一个破解方式都会返回破解出来的明文
    """
    def __init__(self, c, e, p, q):
        assert is_prime(p) and is_prime(q)
        self.c, self.e, self.p, self.q = c, e, p, q

    def crack_by_p(self):
        g = gcd(self.p - 1, self.e)
        d = inverse_mod(Integer(self.e / g), self.p - 1)
        mg = powmod(self.c % self.p, d, self.p)
        CRSE = CrackSmallE(mg, g, self.p, self.p - 1)
        return mg if g == 1 else CRSE.crack()

    def crack_by_q(self):
        g = gcd(self.q - 1, self.e)
        d = inverse_mod(Integer(self.e / g), self.q - 1)
        mg = powmod(self.c % self.q, d, self.q)
        CRSE = CrackSmallE(mg, g, self.q, self.q - 1)
        return mg if g == 1 else CRSE.crack()

    def crack_by_pq(self):
        mp, mq = self.crack_by_p(), self.crack_by_q()
        return crt([mp, mq], [self.p, self.q])

if __name__ == "__main__":
    c, e, p, q = 20, 3, 5, 7
    c = CrackEPhiNotRP(c, e, p, q)
    print c.crack_by_pq()