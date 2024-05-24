from math import cos, sin, atan, sqrt
from scipy.optimize import fsolve

def cot(x):
    return cos(x)/sin(x)

def cot2(x):
    return cot(x)**2

def acot(x):
    return atan(1/x)

def interpolation(xa, xb, ya, yb, x):
    return (ya - yb) / (xa - xb) * x + (xa * yb - xb * ya) / (xa - xb)

def racinepolynome2(a, b, c, i):
    delta = b**2 - (4 * a * c)
    x1 =(-b + sqrt(delta)) / (2 * a)
    x2 =(-b - sqrt(delta)) /( 2 * a)
    resultat = [x1, x2]
    return resultat[int(i)-1]

def racinepolynome3(a, b, c, d, i):
    def f(x, a, b, c, d):
        return a * x**3. + b * x**2. + c * x + d
    return fsolve(f, 0.2, argamma_s = (a, b, c, d))[i]