from sympy import *


class Solver:

    def __init__(self, equation=""):
        self.equationSolvedLatex = None
        self.equationLatex = None
        solve(equation)

    def solve(self, equation: str):
        self.equationLatex = latex(equation)
        y = Function('y')
        x = symbols('x')
        self.equationSolvedLatex = (latex(dsolve(equation, y(x))))

    def solve_and_get(self, equation: str):
        self.solve(equation)
        return self.equationSolvedLatex

    def get_equation_latex(self):
        return self.equationLatex

    def get_solution_latex(self):
        return self.equationSolvedLatex
