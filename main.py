import cvxpy as cp
import numpy as np

from functools import reduce
from argparse import ArgumentParser


class Solution:
    def __init__(self, bundle, problem, total_count):
        self.bundle = bundle
        self.solved = problem
        self.total_count = total_count

    def print(self):
        avg_price = self.__float__()
        int_price = self.__int__()
        fraction = int_price * self.total_count - self.solved.value

        print("total price: {:.0f}".format(self.solved.value))
        print("avarage price: {} ({:.6f})".format(int_price, avg_price))
        print("fraction: {:.0f}".format(fraction))

        for count, price, var in self.bundle.list:
            print("{:d} bundle: {:.0f}".format(count, var.value))
        print('=' * 40)

    def __float__(self):
        return self.solved.value / self.total_count

    def __int__(self):
        return int(np.ceil(self.__float__()))


class Bundles:
    def __init__(self, tuples):
        self.list = [(count, price, cp.Variable(integer=True))
                     for count, price in tuples]

    def constraints(self, total_count):
        return [
            reduce(lambda x, y: x + y[0] * y[2], self.list, 0) == total_count,
            *(var >= 0 for count, price, var in self.list)
        ]

    def objective(self):
        return cp.Minimize(
            reduce(lambda x, y: x + y[0] * y[1] * y[2], self.list, 0),
        )

    def solve(self, total_count, **args):
        problem = cp.Problem(self.objective(), self.constraints(total_count))
        problem.solve(**args)

        return Solution(self, problem, total_count)


if __name__ == '__main__':
    parser = ArgumentParser(description="Get optimal method to buy bundles")
    parser.add_argument(
        'total_amount',
        metavar='N',
        help="total amount to buy",
        type=int)
    args = parser.parse_args()

    assert args.total_amount > 0, 'N should > 0'

    bundles = Bundles([
        (1, 564),
        (2, 540),
        (3, 504),
        (4, 491),
        (8, 472),
    ])

    bundles.solve(args.total_amount).print()
