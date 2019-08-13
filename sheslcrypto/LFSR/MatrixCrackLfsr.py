#!/usr/bin/env python2
#coding=utf-8
from sage.all import *


class MatrixCrackLfsr:
    """
    通过矩阵乘积的方式，求解 lfsr 的转移矩阵

    :param seq: 已经捕获的比特流序列，一个 0,1 数字构成的列表
    :param period: 用户可以指定序列的周期，如果周期不对，则会报出 Assert 错误

    :return 序列对应的状态转移矩阵
    """
    def __init__(self, seq, period=None):
        self.period = period
        self.gf2 = GF(2)
        assert (len(seq) & 1) == 0
        self.seq = [self.gf2(c) for c in seq]

    def crack_by_matrix(self):
        maxp = len(self.seq) / 2
        S0 = Matrix([self.seq[i:i + maxp] for i in range(maxp)])
        S1 = Matrix([self.seq[i:i + maxp] for i in range(maxp + 1)[1:]])
        rs0, rs1 = S0.rank(), S1.rank()
        assert (rs0 == rs1) and (self.period is None or self.period == rs0)
        self.period = rs0

        if self.period != maxp:
            S0 = Matrix([self.seq[i:i + self.period] for i in range(self.period)])
            S1 = Matrix([self.seq[i:i + self.period] for i in range(self.period + 1)[1:]])
            assert S0.rank() == S1.rank()
        return S0.solve_right(S1)


if __name__ == "__main__":
    CL = MatrixCrackLfsr([1, 0, 1, 0, 0, 0, 1, 0])
    print CL.crack_by_matrix()
