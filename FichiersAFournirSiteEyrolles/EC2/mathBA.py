#-*- Encoding: Utf-8 -*-

from scipy.optimize import fsolve

def solve3deg(a, b, c, d):
    def f(x, a, b, c, d):
        return a * x**3.0 + b * x**2.0 + c * x + d
    return fsolve(f, 0.2, args=(a, b, c, d))[0]