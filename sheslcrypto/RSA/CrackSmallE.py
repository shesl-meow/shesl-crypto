#!/usr/bin/env python2
#coding=utf-8
from gmpy2 import iroot, gcd, powmod


class CrackSmallE:
    """
    这个类用于 RSA 系统的加密指数比较小的时候

    :param c: RSA 系统的密文
    :param e: RSA 系统的指数，要求这个 e 比较小
        如果指数较大，破解只会陷入高时间复杂度中而不会报错
    :param n: RSA 系统中的模数，一般是两个素数的积
    :param phi: n 的欧拉函数，如果提供了欧拉函数，则会检测方程是否有解

    :return m: 调用 crack() 函数进行爆破，返回明文
    """
    def __init__(self, c, e, n, phi=None):
        self.c, self.e, self.n, self.phi = c, e, n, phi

    def check_remainder(self):
        if self.phi is None: return
        d = gcd(self.e, self.phi)
        assert powmod(self.c, int(self.phi / d), self.n) == 1

    def crack_times(self):
        k = -1
        while True:
            k += 1
            res, check = iroot(k * self.n + self.c, self.e)
            if check: break
        self.m = res

    def crack(self):
        self.check_remainder()
        self.crack_times()
        return self.m

if __name__ == "__main__":
    c, e, n = 13, 3, 15
    cse = CrackSmallE(c, e, n)
    print(cse.crack())