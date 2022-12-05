import signal

from sympy import *


class DSolver:
    @staticmethod
    def to_latex(equation: str):
        """

        :param equation: any expression
        :return: latex form of the given expression
        """
        return latex(equation.replace(" ", ""))

    @staticmethod
    def solve(equation: str):
        """

        :param equation:
        :return: solution in latex if entered equation is solvable, empty str if not
        """
        try:
            to_solve = DSolver.recognize_symbols(equation)
            if to_solve is None:
                return ""
            solution = DSolver.solve_from_string(to_solve)
            return latex(solution)
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def recognize_symbols(equation: str):
        formatted = equation.replace(" ", "")
        formatted = formatted.replace("’", "'")
        formatted = DSolver.insert_skipped_multiply(formatted)
        formatted = formatted.replace("^", "**")
        formatted = formatted.replace("e", "E")
        formatted = formatted.replace("y'", "diff(y, x)")
        if DSolver.can_cut_differentials(formatted):
            formatted = formatted.replace("dx", "1")
            formatted = formatted.replace("dy", "diff(y, x)")
            formatted = formatted.replace("y", "y(x)")
            return formatted
        else:
            return None

    @staticmethod
    def can_cut_differentials(equation: str):
        if not equation.__contains__("dx") and not equation.__contains__("dy"):
            return True
        modified = equation.replace("dx", "1")
        modified = modified.replace("dy", "(M/V)")
        modified = modified.replace("y", "y")
        expected = equation.replace("dx", "V")
        expected = expected.replace("dy", "M")
        expected = expected.replace("y", "y")
        eq1 = DSolver.to_equation(expected)
        eq2 = DSolver.to_equation(modified)
        res1 = solve(eq1)
        res2 = solve(eq2)
        return res1 == res2

    @staticmethod
    def to_equation(input_str: str):
        parts = input_str.split("=")
        if len(parts) != 2:
            return ""
        return Eq(parse_expr(parts[0]), parse_expr(parts[1]))

    @staticmethod
    def solve_from_string(equation):
        deq = DSolver.to_equation(equation)
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
            elif equation[i] in "exy)'" and equation[i + 1] in '012345689abcdABCDxy':
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
