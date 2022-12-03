from unittest import TestCase

from sympy import *

from dsolver import DSolver


class TestSolver(TestCase):
    def test_solve(self):
        t = symbols('t')
        z = Function('z')
        deq = Eq(parse_expr("diff(z(t), t)"), parse_expr("z(t)"))
        xsoln = dsolve(deq, z(t))
        print(latex(xsoln))
    def test_simple(self):
        print(DSolver.solve("y'=y"))

    def test_complex(self):
        print(DSolver.solve("y'+y*tan(x)=1/cos(x)"))
