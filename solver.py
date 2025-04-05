from sympy import symbols, Eq, solve
import re

equations_str = input("Enter equations to solve (comma-separated): ")
equations_str = equations_str.replace("=", "==")
equations_str = re.sub(r'(?<!\*)\b(\d+)([a-zA-Z])', r'\1*\2', equations_str)
equations_str = equations_str.replace("^", "**")

equation_list = equations_str.split(",")
variables = sorted(set(re.findall(r'\b[a-zA-Z]+\b', equations_str)))
symbols_dict = {var: symbols(var) for var in variables}

equations = []
try:
    for eq in equation_list:
        lhs, rhs = eq.strip().split("==")
        equations.append(Eq(eval(lhs, {**symbols_dict}), eval(rhs, {**symbols_dict})))
    
    solutions = solve(equations, list(symbols_dict.values()))
    print("Solutions:")
    
    if isinstance(solutions, dict):
        for var, sol in solutions.items():
            print(f"{var} = {sol}")
    elif isinstance(solutions, list):
        for sol in solutions:
            print(sol)
    else:
        print(solutions)
except Exception as e:
    print("Invalid equation format. Please try again.")