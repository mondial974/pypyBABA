#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: compression.py
"""
Module pour calculer les sections d'acier de poteaux circulaires et rectangulaires
"""
__version__ = '0.1'

from scipy.optimize import fsolve
from math import pi
from EC2.materiaux import fcd, fyd

def alphaRect(Lambda1):
    """ coefficient de réduction en fonction de l'élancement
    entrée : lambda1 []
    sortie : []"""
    if (Lambda1 < 60.):
        return 0.86 / (1.0 + (Lambda1 / 62.0)**2.0)
    else:
        return (32 / Lambda1)**1.3
    
def alphaCirc(Lambda1):
    """ coefficient de réduction en fonction de l'élancement
    entrée : lambda1 []
    sortie : []"""
    if (Lambda1 < 60.):
        return 0.84 / (1.0 + (Lambda1 / 52.0)**2.0)
    else:
        return (27 / Lambda1)**1.24

def khRect(h, rho, delta):
    """ réductoin en fonction de la hauteur de la section
    entrée : h [m], rho, delta []
    sortie : []"""
    if (h < 0.5):
        return (0.75 + 0.5 * h) * (1.0 - 6.0 * rho * delta)
    else:
        return 1.0

def khCirc(D, rho, delta):
    """ réductoin en fonction du diamètre de la section
    entrée : D [m], rho, delta []
    sortie : []"""
    if (D < 0.6):
        return (0.7 + 0.5 * D) * (1.0 - 8.0 * rho * delta)
    else:
        return 1.0

ksRect = 1.0 #provisoire  
ksCirc = 1.0

def rhomin(Ac, NEdu, fyk):
    """ pourcentage minimum 
    entrée : Ac [m²], NEdu [MN], fyk [MPa]
    sortie : []"""
    return max(0.1 * NEdu / fyd(fyk) / Ac, 0.002)
    
def rhomax():
    """ pourcentage minimum 
    entrée : Ac [m²], NEdu [MN], fyk [MPa]
    sortie : []"""
    return 0.04

def NRdRect(rho, bp, hp, dp, fck, fyk, Lambda1, ksRect):
    """ effort normal résistant de la section rectangulaire
    entrée : rho [] bp, hp, dp [m], fck, fyk [MPa], lambda, ksrect []
    sortie : [MN]"""
    dpmax=min(0.3 * hp, 0.1)
    if (dp > dpmax):
        print("Attention dp trop grand... dp={0:.3f} m > min(0.3h, 0.1) = {1:.3f}".format(dp,dpmax))
        dp = dpmax
    delta = dp / hp
    return bp * hp * ksRect * khRect(hp, rho, delta) \
            * alphaRect(Lambda1) * (fcd(fck) + rho * fyd(fyk))

def EqNRect(rho, NEdu, bp, hp, dp, fck, fyk, Lambda1, ksRect):
    """ equation d'équilibre en effort normal"""
    return NEdu - NRdRect(rho, bp, hp, dp, fck, fyk, Lambda1, ksRect)

def rhoRectSol(NEdu, bw, h, dp, fck, fyk, Lambda1, ksRect):
    return fsolve(EqNRect, 0.001, args=(NEdu, bw, h, dp, fck, fyk, Lambda1, ksRect))[0]

def rhoRect(NEdu, bp, hp, dp, fck, fyk, Lambda1, aff = False):
    """ Détermination des sections d'acier pour une section rectangulaire (Thonier)
     entrée : NEdu [MN], D, dp [m], fck, fyl [MPa], Lambda []
     sortie : rho []"""
    if (aff):
        print("Calcul en section rectangulaire : algorithme de Thonier")
        print(" Attention le As / 2 sur chaque face dans la direction de flambement")
        print(" poteau de bâtiment bi-articulé sous charges centrées ")
        print(" chargement à au moins 28 jours")
        print(" ciment (N)ormaux et (R)apide")
        print(" taux d’humidité relative : 40 < RH < 100%")
    if (fck > 50) or (fck < 20):
        print(" Algorithme non applicable 20 < fck < 50 MPa or fck = {:.0f} MPa".format(fck))
    if (hp < .15):
        print(" Algorithme non applicable h > 150 mm or h = {:.0f} mm".format(hp * 1e3))
    Ac = bp * hp
    rhomin1 = rhomin(Ac, NEdu, fyk)
    rhomax1 = rhomax()
    rho = fsolve(EqNRect, 0., args=(NEdu, bp, hp, dp, fck, fyk, Lambda1, ksRect))[0]
    if (rho < rhomin1):
        if (aff):
            print("rho = {0:.3f} < rhomin = {1:.3f}".format(rho, rhomin1))
            print("As > {0:.2f} mm² (As/2 sur chaque face)".format(rhomin1 * Ac * 1e6))
        return rhomin1
    if (rho>rhomax1):
        if (aff):
            print("rho = {0:.3f} > rhomax = {1:.3f}".format(rho, rhomax1))
            print("As > {0:.2f} mm² (As/2 sur chaque face)".format(rhomax1 * Ac * 1e6))
        return rhomax1
    if (aff):
        print("rhomin = {0:.3f}% rho = {1:.3f}% rhomax = {2:.3f}%"
              .format(rhomin1 * 1e2, rho * 1e2, rhomax1 * 1e2))
        print("As > {0:.2f} mm² (As/2 sur chaque face)".format(rho * Ac * 1e6))
    return rho


def AsCompRect(NEdu, bp, hp, dp, fck, fyk, Lambda1, aff = False):
    """ Détermination des sections d'acier pour une section rectangulaire (Thonier)
     entrée : NEdu [MN], D, dp [m], fck, fyl [MPa], Lambda []
     sortie : As [m²]"""
    return rhoRect(NEdu, bp, hp, dp, fck, fyk, Lambda1, aff) * bp * hp



def NRdCirc(rho, D, dp, fck, fyk, Lambda1, ksCirc):
    """ effort normal résistant de la section criculaire
    entrée : rho [] Dp, dp [m], fck, fyk [MPa], lambda, ksrCirc []
    sortie : [MN]"""
    dpmax=min(0.3 * D, 0.1)
    if (dp > dpmax):
        print("Attention dp trop grand... dp={0:.3f} m > min(0.3D, 0.1)={1:.3f}".format(dp,dpmax))
        dp = dpmax
    delta = dp / D
    return pi * D**2.0 / 4 * ksCirc * khCirc(D, rho, delta) \
            * alphaCirc(Lambda1) * (fcd(fck) + rho * fyd(fyk))

def EqNCirc(rho, NEdu, D, dp, fck, fyk, Lambda1, ksCirc):
    """ equation d'équilibre en effort normal"""
    return NEdu - NRdCirc(rho, D, dp, fck, fyk, Lambda1, ksCirc)

def rhoCirc(NEdu, D, dp, fck, fyk, Lambda1, aff = False):
    """ Détermination des sections d'acier pour une section circulaire (Thonier)
     entrée : NEdu [MN], D, dp [m], fck, fyl [MPa], Lambda []
     sortie : rho []"""
    if (aff):
        print("Calcul en section circulaire : algorithme de Thonier")
        print(" Attention 6 barres à minima réparties sur la circonférence")
        print(" poteau de bâtiment bi-articulé sous charges centrées ")
        print(" chargement à au moins 28 jours")
        print(" ciment (N)ormaux et (R)apide")
        print(" taux d’humidité relative : 40 < RH < 100%")
    if (fck > 50) or (fck < 20):
        print(" Algorithme non applicable 20 < fck < 50 MPa or fck = {:.0f} MPa".format(fck))
    if (D < .15):
        print(" Algorithme non applicable h > 150 mm or h = {:.0f} mm".format(D * 1e3))
    if (aff):
        print("Calcul en section circulaire : algorithme de Thonier")
    Ac = pi * D * D / 4.0
    rhomin1 = rhomin(Ac, NEdu, fyk)
    rhomax1 = rhomax()
    rho = fsolve(EqNCirc, 0., args=(NEdu, D, dp, fck, fyk, Lambda1, ksCirc))[0]
    if (rho < rhomin1):
        if (aff):
            print("rho = {0:.3f} < rhomin = {1:.3f}".format(rho, rhomin1))
            print("As > {0:.2f} mm² (6 barres mini)".format(rhomin1 * Ac * 1e6))
        return rhomin1
    if (rho > rhomax1):
        if (aff):
            print("rho = {0:.3f} > rhomax = {1:.3f}".format(rho, rhomax1))
            print("As > {0:.2f} mm² (6 barres mini)".format(rhomax1 * Ac * 1e6))
        return rhomax1
    if (aff): 
        print("rhomin = {0:.3f}e-2 rho = {1:.3f}e-2 rhomax = {2:.3f}e-2"
              .format(rhomin1 * 1e2, rho * 1e2, rhomax1 * 1e2))
        print("As > {0:.2f} mm² (6 barres mini)".format(rho * Ac * 1e6))
    return rho

def AsCompCirc(NEdu, D, dp, fck, fyk, Lambda1, aff = False):
    """ Détermination des sections d'acier pour une section circulaire (Thonier)
     entrée : NEdu [MN], D, dp [m], fck, fyl [MPa], Lambda []
     sortie : As [m²]"""
    return rhoCirc(NEdu, D, dp, fck, fyk, Lambda1, aff) * pi * D * D / 4.
 
if __name__ == "__main__":
    print("Exemple 1")
    NEdu = 1.04 #MN
    dp = 50e-3 
    L = 3.00 #m
    Lo = 0.7 * L     
    #béton 
    fck = 25 #MPa
    fyk = 500.
    bp, hp = 0.250, .250 #m
    Lambda1 = Lo / bp * 12**.5
    As = AsCompRect(NEdu, bp, hp, dp, fck, fyk, Lambda1, aff = True)