from unittest import TestCase

from sympy import *

from dsolver import DSolver


class TestSolver(TestCase):
    def test_solve(self):
        t = symbols('t')
        z = Function('z')
        deq = Eq(parse_expr("diff(z(t), t)"), parse_expr("z(t)"))
        solution = dsolve(deq, z(t))
        print(latex(solution))

    def test_simple(self):
        print(DSolver.solve("y'=y"))

    def test_complex(self):
        print(DSolver.solve("y'+y*tan(x)=1/cos(x)"))

    def test_real_examples9(self):
        print(DSolver.solve("y' = x - e^y"))

    def test_real_examples25(self):
        print(DSolver.solve("y'=ax^2 + be^x"))

    def test_real_examples50(self):
        print(DSolver.solve("y' = Cx + C^3"))

    def test_real_examples64(self):
        print(DSolver.solve("(x+2y)y' = 1"))

    def test_real_examples103(self):
        print(DSolver.solve(" (x y +e^x) dx - xdy = y"))

    def test_infinite(self):
        print(DSolver.solve("y'^4=y"))
