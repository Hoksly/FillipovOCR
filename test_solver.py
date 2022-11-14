from unittest import TestCase

from sympy import *


class TestSolver(TestCase):
    def test_solve(self):
        t = symbols('t')
        z = Function('z')
        deq = Eq(parse_expr("diff(x(t), t)"), parse_expr("z(t)"))
        xsoln = dsolve(deq, z(t))
        print(latex(xsoln))

