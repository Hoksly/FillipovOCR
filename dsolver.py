from sympy import *


class DSolver:

    @staticmethod
    def to_latex(expression):
        """

        :param expression: any equation
        :return: the same expression in latex
        """
        return latex(expression)

    @staticmethod
    def solve(equation: str):
        """

        :param equation:
        :return: solution in latex if entered equation is solvable, empty str if not
        """
        to_solve = DSolver.recognize_symbols(equation)
        try:
            solution = DSolver.solve_equation(to_solve)
            return latex(solution)
        except ValueError:
            return ""


    @staticmethod
    def recognize_symbols(equation: str):
        formatted = equation.replace("y'", "diff(y, x)")
        formatted = formatted.replace("y", "y(x)")
        return formatted

    @staticmethod
    def solve_equation(equation):
        parts = equation.split("=")
        assert len(parts) == 2
        deq = Eq(parse_expr(parts[0]), parse_expr(parts[1]))
        return dsolve(deq)

