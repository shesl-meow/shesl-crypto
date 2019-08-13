#!/usr/bin/env python2
# coding=utf-8
from sage.all import *


class FactorByPHighBits:
    """
    如果 RSA 系统中的 p 的高位是已知的，则可以使用这个类尝试分解 N。其原理是使用了
        《Mathematics_of_Public_Key_Cryptography》 书中的 Coppersmith 攻击
    """
    def __init__(self, n, p_high, p_bitlen=None):
        """
        :param n: RSA 系统中的模数
        :param p_high: p 的已知高位（比如已知最高两位为 0b11, 则应该传入 3）
        :param p_bitlen: p 的比特位长度，不指定则为 n 比特位长度的一半
        """
        self.n, self.p_high = Integer(n), Integer(p_high)
        self.p_bitlen = int(self.n.bits() / 2) if p_bitlen is None else p_bitlen
        zmod = Zmod(n)
        self.PR = PolynomialRing(zmod, 'x')

    def factorization(self):
        """
        对传入的整数 n 进行分解。
        :return:返回两个素数 p,q，前者小于后者
        """
        x = self.PR.gen()
        ubits = self.p_bitlen - self.p_high.nbits()
        lp = self.p_high << ubits
        f = lp + x
        beta = float(log(lp, self.n))
        roots = f.small_roots(X=2**ubits, beta=beta)
        if roots:
            p = Integer(lp + roots[0])
            q = Integer(self.n / p)
            return (p,q) if p<q else (q,p)
        else: assert False



if __name__ == "__main__":
    p, q = 64663, 34157
    p_high = p >> (p.bit_length() - int(p.bit_length() / 2**0.5))
    f = FactorByPHighBits(p * q, p_high, p_bitlen=p.bit_length())
    print f.factorization()
