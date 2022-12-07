##### DSolver
The class uses [**Sympy**](https://www.sympy.org/en/index.html) library to solve differential equations.
The input string is parsed to differential equation. *y* and *x* are considered as function and its independent variable.
Any other letter is considered as constant.
If input string contains *dy* or *dx*, the solver will attempt to extract the derivative (*dy/dx*).
Extra spaces won't affect the solution.
Skipped multiply operations will be added automatically.
The solution of the given differential equation is parsed to LaTeX string. If the input string cannot be parsed or solved, the method returns an empty string.
