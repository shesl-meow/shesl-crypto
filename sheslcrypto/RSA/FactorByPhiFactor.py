#!/usr/bin/env python
# coding=utf-8
from gmpy2 import next_prime, powmod, gcd


class FactorByPhiFactor:
    """
    如果已知 p-1 或 q-1 的最大因子，或者我们知道 p-1, q-1 有很多的小因子。
        则我们可以通过这个类来分解 N。
    该类数学原理是使用了 Pollard's p − 1 algorithm 这个算法。
    """

    def __init__(self, n, bound=None):
        """
        :param n: RSA 系统中两个大素数的积
        :param bound: 算法的参数，该数越大越有可能分解出 p,q，但会增加时间复杂度。
            1. 算法指出，该参数最合适的值是 p或q 最大素因子的数量级。
                bound 不应该大于最大的素因子（严格的），也不应该过小不到该数量级。
            2. 如果没有传入 bound，将其设置为 None，则程序会逐一尝试
        """
        self.n, self.B = n, bound

    def factor_with_bound(self):
        """
        m = \Prod_{1 \le p \le B, \text{p is prime}} p^{ceil{log_p B}}

        :return: 返回两个素数 p,q，前者小于后者。无法分解则返回 None
        """
        assert self.B is not None
        p, m = 2, 1  # p 最小的素数
        while p < self.B:
            prev_p, prod_p = 1, p
            while prod_p <= self.B:
                prev_p = prod_p
                prod_p *= p
            m *= prev_p
            p = next_prime(p)
        am = powmod(2, m, self.n)
        p = gcd(am - 1, self.n)
        if p == 1 or p == self.n:
            return None
        q = self.n / p
        return (p, q) if p < q else (q, p)

    def factor_without_bound(self, verbose=False):
        """
        尝试通过穷举 bound 的方式，爆破出合适的 bound

        :return:返回两个素数 p,q，前者小于后者。
        """
        prl, pml, next_pml = [2, 3]+4094*[1], [1]*4096, [2,3]+[1]*4094
        pos = 2
        am = powmod(2, 1, self.n)
        while True:
            for i in range(pos):
                while next_pml[i] <= prl[pos-1]:
                    pml[i] = next_pml[i]
                    am = powmod(am, prl[i], self.n)
                    next_pml[i] *= prl[i]
            p = gcd(am - 1, self.n)
            if p != 1 and p != self.n: break

            pr = next_prime(prl[pos - 1])
            prl[pos], next_pml[pos] = pr, pr
            pos += 1
            if pos == len(pml):
                prl += [1]*pos
                pml += [1]*pos
                next_pml += [1]*pos

            if verbose and pos%1000==0:
                print "prime pos, prime, gcd: %d, %d, %d" % (pos, pr, p)
            # assert powmod(2, reduce(lambda a,b: a*b, pml), self.n) == am

        q = self.n / p
        return (p,q) if p<q else (q,p)

    def factorization(self):
        return self.factor_with_bound() \
            if self.B is not None else \
            self.factor_without_bound()


if __name__ == "__main__":
    p_lst = [2]
    for i in range(171):
        p_lst.append(next_prime(p_lst[i]))
    from functools import reduce

    p = reduce(lambda a, b: a * b, p_lst[:-1]) + 1
    q = reduce(lambda a, b: a * b, p_lst) + 1
    print p.bit_length(), p
    print q.bit_length(), q

    from gmpy2 import is_prime

    assert is_prime(p) and is_prime(q)
    f = FactorByPhiFactor(p * q, p_lst[-1])
    print "factor with bound: "
    p, q = f.factorization()
    print p.bit_length(), p
    print q.bit_length(), q

    print "factor without bound: "
    f = FactorByPhiFactor(p * q)
    p, q = f.factorization()
    print p.bit_length(), p
    print q.bit_length(), q
