from math import pi, radians, exp, tan, atan, sqrt, degrees

# Calcul coef idelta d'inclinaison de charge # TERMINE
def idc(dd):
    return (1 - 2 * dd / pi)**2

def idf(dd, De, B):
    if dd < pi / 4:
        return (1 - 2 * dd / pi)**2 - 2 * dd / pi * (2 - 3 * 2 * dd / pi) * exp(-De / B)
    else:
        return (1 - 2 * dd / pi)**2 - (1 - 2 * dd / pi)**2 * exp(-De / B)

def idcf(dd, De, B, c, gamma, phi):
    a = 0.6
    return idf(dd , De ,B) + (idc(dd) - idf(dd , De ,B)) * (1 - exp(- a * c / (gamma * B * tan(phi))))

def id(dd, De, B, c, gamma, phi):
    if phi == 0 and c > 0:
        return idc(dd)
    
    if phi > 0 and c == 0:
        return idf(dd, De, B)
    
    if phi > 0 and c > 0:
        return idcf(dd, De, B, c, gamma, phi)

Hx = 17.52 / 100
Hy = 7.37 / 100
Hd = sqrt(Hx**2 + Hy**2)

Vd = 83.78 / 100

dd = atan(Hd / Vd)
De = 160 / 100
B = 858 / 100
gamma = 1.8 / 100
c = 0 / 1000
phi = radians(30)

print(degrees(dd))
print(id(dd, De, B, c, gamma, phi))