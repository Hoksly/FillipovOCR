import signal

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
            solution = DSolver.solve_from_string(to_solve)
            return latex(solution)
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def recognize_symbols(equation: str):
        formatted = equation.replace(" ", "")
        formatted = formatted.replace("dx", "1")
        formatted = formatted.replace("dy", "y'")
        formatted = DSolver.insert_skipped_multiply(formatted)
        formatted = formatted.replace("^", "**")
        formatted = formatted.replace("e", "E")
        formatted = formatted.replace("y'", "(diff(y, x))")
        formatted = formatted.replace("y", "y(x)")
        return formatted

    @staticmethod
    def solve_from_string(equation):
        parts = equation.split("=")
        if len(parts) != 2:
            return ""
        deq = Eq(parse_expr(parts[0]), parse_expr(parts[1]))
        DSolver.called_solver = False
        result = DSolver.solve_equation(deq)
        if result is None and not DSolver.called_solver:
            result = dsolve(deq)
        return result

    called_solver = True

    @staticmethod
    def time_break(func):
        def wrapper(*args, **kwargs):
            try:
                signal.alarm(10)
                DSolver.called_solver = True
                result = func(*args, **kwargs)
                signal.alarm(0)
                return result
            except Exception:
                return None

        return wrapper

    @staticmethod
    @time_break
    def solve_equation(deq: Eq):
        return dsolve(deq)

    @staticmethod
    def insert_skipped_multiply(equation: str):
        s = ""
        a = len(equation) - 1
        for i in range(0, a):
            s += equation[i]
            if equation[i + 1] in "exy(" and equation[i] in '012345689abcABCDxy':
                s += '*'
            elif equation[i] in "exy)'" and equation[i + 1] in '012345689abcABCDxy':
                s += '*'
        s += equation[a]
        return s

    @staticmethod
    def to_derivative_from(equation: str):
        s = ""
        a = len(equation) - 1
        for i in range(0, a):
            s += equation[i]
            if equation[i + 1] in "exy(" and equation[i] in '012345689abcABCDxy':
                s += '*'
            elif equation[i] in "exy)'" and equation[i + 1] in '012345689abcABCDxy':
                s += '*'
        s += equation[a]
        return s
