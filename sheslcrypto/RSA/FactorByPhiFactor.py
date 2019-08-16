#!/usr/bin/env python
# coding=utf-8
from random import randint
from gmpy2 import next_prime, powmod, gcd


class FactorByPhiFactor:
    """
    如果已知 p-1 或 q-1 的最大因子，或者我们知道 p-1, q-1 有很多的小因子。
        则我们可以通过这个类来分解 N。
    该类数学原理是使用了 Pollard's p − 1 algorithm 这个算法。
    """

    def __init__(self, n, bound):
        """
        :param n: RSA 系统中两个大素数的积
        :param bound: 算法的参数，该数越大越有可能分解出 p,q，但会增加时间复杂度。
            算法指出，该参数最合适的值是 p或q 最大素因子的数量级。
            bound 不应该大于最大的素因子（严格的），也不应该过小不到该数量级。
        """
        self.n, self.B = n, bound

    def calculate_m(self):
        """
        :return: m = \Prod_{1 \le p \le B, \text{p is prime}} p^{ceil{log_p B}}
        """
        p, m = 2, 1  # p 最小的素数
        while p < self.B:
            prev_p, prod_p = 1, p
            while prod_p <= self.B:
                prev_p = prod_p
                prod_p *= p
            m *= prev_p
            p = next_prime(p)
        return m

    def factorization(self):
        """
        尝试三个不同的 a，如仍然无法分解返回 None

        :return: 返回两个素数 p,q，前者小于后者
        """
        m = self.calculate_m()
        for _ in range(3):
            a = randint(1, self.n)
            p = gcd(a, self.n)
            if p != 1 and p != self.n:
                break
            am = powmod(a, m, self.n)
            p = gcd(am - 1, self.n)
            if p != 1 and p != self.n:
                break
            p = None
        if p is not None:
            q = self.n / p
            return (p, q) if p < q else (q, p)
        else: return None


if __name__ == "__main__":
    p_lst = [2]
    for i in range(171):
        p_lst.append(next_prime(p_lst[i]))
    from functools import reduce
    p = reduce(lambda a,b: a*b, p_lst[:-1]) + 1
    q = reduce(lambda a,b: a*b, p_lst) + 1
    print p.bit_length(), p
    print q.bit_length(), q

    from gmpy2 import is_prime
    assert is_prime(p) and is_prime(q)
    f = FactorByPhiFactor(p * q, p_lst[-1])
    p,q = f.factorization()
    print p.bit_length(), p
    print q.bit_length(), q
