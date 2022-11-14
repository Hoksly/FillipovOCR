from sympy import *


class Solver:

    def __init__(self, equation=""):
        self.solutionLatex = None
        self.equationLatex = None
        solve(equation)

    def solve(self, equation: str):
        self.equationLatex = latex(equation)
        self.solutionLatex = (latex(dsolve(equation)))

    def solve_and_get(self, equation: str):
        self.solve(equation)
        return self.solutionLatex

    def get_equation_latex(self):
        return self.equationLatex

    def get_solution_latex(self):
        return self.solutionLatex
