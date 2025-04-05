"""
Module: x
Calculates π (pi) using several different algorithms.
Available methods:
  - chudnovsky: Uses the Chudnovsky algorithm.
  - bbp: Uses the Bailey–Borwein–Plouffe algorithm.
  - leibniz: Uses the Leibniz series.
  - nilakantha: Uses the Nilakantha series.
  - machin: Uses Machin's formula (arctan series).
  - gauss_legendre: Uses the Gauss–Legendre algorithm.

Each method accepts:
  - digits (int): Number of significant digits desired.
  - n_terms / n_iterations (int): Number of terms/iterations in the algorithm.

Usage:
  import x

  # Chudnovsky algorithm:
  print(x.compute_pi(method="chudnovsky", n_terms=10, digits=50))

  # BBP algorithm:
  print(x.compute_pi(method="bbp", n_terms=20, digits=50))

  # Leibniz series:
  print(x.compute_pi(method="leibniz", n_terms=1000, digits=50))

  # Nilakantha series:
  print(x.compute_pi(method="nilakantha", n_terms=1000, digits=50))

  # Machin's formula:
  print(x.compute_pi(method="machin", n_terms=100, digits=50))

  # Gauss–Legendre algorithm:
  print(x.compute_pi(method="gauss_legendre", n_iterations=5, digits=50))
"""

from decimal import Decimal, getcontext, ROUND_HALF_UP
import math

__all__ = [
    "pi_chudnovsky", "pi_bbp", "pi_leibniz", "pi_nilakantha",
    "pi_machin", "pi_gauss_legendre", "compute_pi", "available_methods"
]

# Helper function: round a Decimal to a given number of significant digits.
def round_decimal(x: Decimal, digits: int) -> Decimal:
    """
    Round a Decimal x to the specified number of significant digits.
    """
    if x == 0:
        return x
    # Determine the exponent (in scientific notation).
    exp = x.adjusted()
    # Create a quantizer for the desired precision.
    quantizer = Decimal('1e{}'.format(exp - digits + 1))
    return x.quantize(quantizer, rounding=ROUND_HALF_UP)

def pi_chudnovsky(n_terms=10, digits=50):
    """
    Calculate π using the Chudnovsky algorithm.
    
    Parameters:
      n_terms (int): Number of terms to sum.
      digits (int): Number of significant digits desired.
    
    Returns:
      Decimal: An approximation of π.
    """
    # Use extra precision for intermediate calculations.
    guard = 5
    getcontext().prec = digits + guard

    C = Decimal(426880) * Decimal(10005).sqrt()
    S = Decimal(13591409)
    M = Decimal(1)
    L = Decimal(13591409)
    X = Decimal(1)
    # Pre-calculate constant factor.
    K_const = Decimal(640320) ** 3

    for k in range(1, n_terms):
        M = M * (Decimal(6 * k - 5) * Decimal(2 * k - 1) * Decimal(6 * k - 1)) / (Decimal(k) ** 3 * K_const)
        L += Decimal(545140134)
        X *= Decimal(-262537412640768000)
        S += M * L / X

    pi = C / S
    return round_decimal(+pi, digits)

def pi_bbp(n_terms=10, digits=50):
    """
    Calculate π using the Bailey–Borwein–Plouffe (BBP) algorithm.
    
    Parameters:
      n_terms (int): Number of terms in the series.
      digits (int): Number of significant digits desired.
    
    Returns:
      Decimal: An approximation of π.
    """
    guard = 5
    getcontext().prec = digits + guard

    pi = Decimal(0)
    for k in range(n_terms):
        # Compute each term using Decimal arithmetic.
        term = (Decimal(1) / (Decimal(16) ** k)) * (
            Decimal(4) / (Decimal(8) * k + Decimal(1)) -
            Decimal(2) / (Decimal(8) * k + Decimal(4)) -
            Decimal(1) / (Decimal(8) * k + Decimal(5)) -
            Decimal(1) / (Decimal(8) * k + Decimal(6))
        )
        pi += term
    return round_decimal(pi, digits)

def pi_leibniz(n_terms=1000, digits=50):
    """
    Calculate π using the Leibniz series:
      π = 4 * Σ (-1)^k/(2k+1)
    
    Parameters:
      n_terms (int): Number of terms to sum.
      digits (int): Number of significant digits desired.
    
    Returns:
      Decimal: An approximation of π.
    """
    guard = 5
    getcontext().prec = digits + guard

    pi = Decimal(0)
    for k in range(n_terms):
        term = ((-1) ** k) / Decimal(2 * k + 1)
        pi += term
    pi *= Decimal(4)
    return round_decimal(pi, digits)

def pi_nilakantha(n_terms=1000, digits=50):
    """
    Calculate π using the Nilakantha series:
      π = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...
    
    Parameters:
      n_terms (int): Number of terms to sum (each term corresponds to one fraction).
      digits (int): Number of significant digits desired.
    
    Returns:
      Decimal: An approximation of π.
    """
    guard = 5
    getcontext().prec = digits + guard

    pi = Decimal(3)
    sign = 1
    # The series starts with i=2 and increases by 2 each time.
    for i in range(2, 2 + 2 * n_terms, 2):
        term = Decimal(4) / (Decimal(i) * Decimal(i + 1) * Decimal(i + 2))
        pi += sign * term
        sign *= -1
    return round_decimal(pi, digits)

def _arctan(x: Decimal, n_terms: int) -> Decimal:
    """
    Compute arctan(x) using its Taylor series:
      arctan(x) = Σ (-1)^k * x^(2k+1)/(2k+1)
    
    Parameters:
      x (Decimal): The value for which to compute arctan.
      n_terms (int): Number of terms to sum.
    
    Returns:
      Decimal: An approximation of arctan(x).
    """
    arctan_val = Decimal(0)
    x_power = x  # x^(2k+1) starts with k=0.
    for k in range(n_terms):
        term = ((-1) ** k) * x_power / Decimal(2 * k + 1)
        arctan_val += term
        # Increase power: multiply by x^2.
        x_power *= x * x
    return arctan_val

def pi_machin(n_terms=100, digits=50):
    """
    Calculate π using Machin's formula:
      π = 16 * arctan(1/5) - 4 * arctan(1/239)
    
    Parameters:
      n_terms (int): Number of terms for the arctan Taylor series.
      digits (int): Number of significant digits desired.
    
    Returns:
      Decimal: An approximation of π.
    """
    guard = 5
    getcontext().prec = digits + guard

    one_over_5 = Decimal(1) / Decimal(5)
    one_over_239 = Decimal(1) / Decimal(239)
    arctan1_5 = _arctan(one_over_5, n_terms)
    arctan1_239 = _arctan(one_over_239, n_terms)
    pi = Decimal(16) * arctan1_5 - Decimal(4) * arctan1_239
    return round_decimal(pi, digits)

def pi_gauss_legendre(n_iterations=5, digits=50):
    """
    Calculate π using the Gauss–Legendre algorithm.
    
    Parameters:
      n_iterations (int): Number of iterations (each iteration roughly doubles the number of correct digits).
      digits (int): Number of significant digits desired.
    
    Returns:
      Decimal: An approximation of π.
    """
    guard = 5
    getcontext().prec = digits + guard

    a = Decimal(1)
    b = Decimal(1) / Decimal(2).sqrt()
    t = Decimal(0.25)
    p = Decimal(1)

    for _ in range(n_iterations):
        a_next = (a + b) / 2
        b = (a * b).sqrt()
        t -= p * (a - a_next) ** 2
        a = a_next
        p *= 2

    pi = ((a + b) ** 2) / (4 * t)
    return round_decimal(pi, digits)

def compute_pi(method="chudnovsky", **kwargs):
    """
    Compute π using the specified method.
    
    Parameters:
      method (str): The algorithm to use. Options are:
                    "chudnovsky", "bbp", "leibniz", "nilakantha", "machin", "gauss_legendre".
      kwargs: Additional keyword arguments for the chosen method (such as n_terms/n_iterations and digits).
    
    Returns:
      The computed value of π (Decimal).
    
    Raises:
      ValueError: If an unknown method is specified.
    """
    method = method.lower()
    if method == "chudnovsky":
        return pi_chudnovsky(**kwargs)
    elif method == "bbp":
        return pi_bbp(**kwargs)
    elif method == "leibniz":
        return pi_leibniz(**kwargs)
    elif method == "nilakantha":
        return pi_nilakantha(**kwargs)
    elif method == "machin":
        return pi_machin(**kwargs)
    elif method == "gauss_legendre":
        return pi_gauss_legendre(**kwargs)
    else:
        raise ValueError("Unknown method: {}. Available methods: {}".format(method, available_methods()))

def available_methods():
    """
    Return a list of available methods for calculating π.
    
    Returns:
      list: A list of method names as strings.
    """
    return ["chudnovsky", "bbp", "leibniz", "nilakantha", "machin", "gauss_legendre"]

# Optional: if run as a script, demonstrate usage.
if __name__ == "__main__":
    print("Chudnovsky (10 terms, 50 digits):")
    print(pi_chudnovsky(n_terms=10, digits=50))
    print("\nBBP (20 terms, 50 digits):")
    print(pi_bbp(n_terms=20, digits=50))
    print("\nLeibniz (1000 terms, 50 digits):")
    print(pi_leibniz(n_terms=1000, digits=50))
    print("\nNilakantha (1000 terms, 50 digits):")
    print(pi_nilakantha(n_terms=1000, digits=50))
    print("\nMachin (100 terms, 50 digits):")
    print(pi_machin(n_terms=100, digits=50))
    print("\nGauss–Legendre (5 iterations, 50 digits):")
    print(pi_gauss_legendre(n_iterations=5, digits=50))
