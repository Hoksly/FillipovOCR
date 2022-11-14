
from sympy import *

class Solver:
    
    equationLatex = ""
    equationSolvedLatex = ""


    def solve(self, equation: str):
        x = Symbol('x')
        self.equationLatex = latex(equation)
        self.equationSolvedLatex = (latex(dsolve(equation)))
