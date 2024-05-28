#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: adherence.py
"""
Module pour calculer l'ahdérence acier/béton
"""
__version__ = '0.1'
import EC2.constantes as CST
import EC2.materiaux as MAT
from math import pi, ceil, sin, cos
from scipy.optimize import fsolve
import numpy as np

def eta11(condbet):
    """condition de bétonnage 
    entree : condbeton [B] sortie [] """
    if (condbet == "B"):
        return 1.0
    else:
        return 0.7

def eta2(phi):
    """conditions de diamètre de barres
    entree phi [m] sortie []"""
    if (phi <= 32e-3):
        return 1.
    else:
        return (132. - phi * 1e3)/100.

def fbd1(condbet, phi, fck, aff = False):
    """contrainte ultime d'adhérence
    entrée : condebet [], phi [m] fck [MPa], sortie : [MPa]"""
    return 2.25 * eta11(condbet) * eta2(phi) * MAT.fctd(fck)


def lbrqd1(condbet, phi, fck, sigsd, aff = False):
    """longueur d'ancarge de référencc 8.4.3
    entree condbeton [], phi [m], fck,sigsd [MPa], sortie [MPa]"""
    return phi / 4. * sigsd / fbd1(condbet, phi, fck, aff)

def yHA(yi, h, alf = 0):
    """ état de la barre vis à vis de la bonne adhérence
    entrée : yi, h[m], alf: [rad], sortie: []"""
    if (yi > h):
        raise ValueError("yHA : barre sortant de la poutre")
    if (alf == pi / 2.):
        return 1.0  #bonne adhérence pour barres verticales (poteau)
    def f(h):
        if (h < 250e-3):
            return h
        if (h < 600e-3):
            return 250e-3
        else:
            return h - 300e-3
    if (yi > f(h)):
        return 0.7  #mauvaise adhérnece
    else:
        return 1.0 #bonne adhérence

def eta12(yi, h, alf = 0):
    """condition de bétonnage 
    entree : yi, h [m] alf: [rad], sortie [] """
    if (alf == pi / 2.): #armatures verticales
        return 1.0
    return yHA(yi, h, alf)


def fbd2(yi, h, phi, fck, alf = 0, aff = False):
    """contrainte ultime d'adhérence
    entree yi, h, phi [m],  fck [MPa], alf [rad], sortie [MPa]"""
    return 2.25 * eta12(yi, h, alf) * eta2(phi) * MAT.fctd(fck)

def lbrqd2(yi, h, phi, fck, sigsd, alf = 0, aff = False):
    """longueur d'ancarge de référencc 8.4.3
    entree ygi, h, phi [m],  fck,sigsd [MPa], sortie [m]"""
    return phi / 4. * sigsd / fbd2(yi, h, phi, fck, alf, aff)

def phimmin(phi):
    """ diamètre de mandrin minimal pour les barres de diamètre phi
    entrée : phi [m]
    sortie : [m]"""
    if (phi <= 16e-3):
        return 4. * phi
    else:
        return 7. * phi

def ancragecourbe(theta0, FEd, lbd, h, t, phi, phit, ab, cnom, fck, condbet, aff = False):
    """ définit si l'ancrage est courbe ou non
    entrée : theta0 [rad], lbd, h, t, phi, phit ab, cnom[m], Fed [MN], fck [MPa]
    sortie :"""
    if (lbd - (t + phit + phi / 2.) < 0):
        if (aff):
            print("Ancrage droit")
            return 0.0
    else:
        fcd1 = MAT.fcd(fck)
        phimmin1 = phimmin(phi)
        fbd1r = fbd1(condbet, phi, fck, aff)
        W = 1. / fcd1 * (1. / ab + 1. / (2. * phi))
        phim1 = (FEd - (t + phit - phi / 2.) * pi * phi * fbd1r) * W
        phim1 = phim1 / (1. - pi * phi * fbd1r * W / 2.)
        phim = max(phimmin1, phim1)
        deltaL1 = lbd - (t + phit + (theta0 - 1.) * (phi + phim) / 2.)
        if (deltaL1 <= 5. * phi):
            phimp = (lbd - (t + phit + (theta0 / 2. + 4.5) * phi)) / (theta0 - 1.) * 2.
            phim = max(phimmin1, phimp)
        phimtab = np.array([16, 20 ,25, 32, 40, 50, 63, 80 ,100, 125, 160, 200, 250, 320 ,400, 500 ,630 ,800]) * 1e-3
        iT = np.where(phimtab > phim)[0][0]
        phimChoix = phimtab[iT]
        if (aff):
            deltaT = t - (cnom + phi + phimChoix / 2.)
            deltah1 = h - (2. * cnom + 2. * phi + phimChoix + phit)
            deltaL = lbd - (t + phit + (theta0 - 1.) * (phi + phimChoix) / 2.)
            deltah2 = (h - 2. * cnom - phit) -  \
                      ((phi + phimChoix / 2.) * (1. - cos(theta0)) + deltaL * sin(theta0))
            print("Diamètre du mandrin : phi_m = {:.2f} mm".format(phimChoix * 1e3))
            print("                    : phi_m1 = {:.2f} mm".format(phim1 * 1e3))
            print("                    : phi_m,min = {:.2f} mm".format(phimmin1 * 1e3))
            if (deltaL1 <= 5. * phi):
                print("                    : phi_m,p = {:.2f} mm".format(phimp * 1e3))
            print("             calcul : phi_m = {:.2f} mm".format(phim * 1e3))
            print("                    : W = {:.3f}".format(W))
            print("                    : DeltaL = {:.3f}".format(deltaL1))          
            print("  ------- vérifications ----")
            print(" Delta_t = {:.2f} mm > ? 0".format(deltaT * 1e3))
            print(" Delta_h1 = {:.2f} mm > ? 0".format(deltah1 * 1e3))           
            print(" Delta_L = {:.2f} mm > ? {:.3f} = 5 phi".format(deltaL * 1e3, 5. * phi * 1e3))           
            print(" Delta_h2 = {:.2f} mm > ? 0".format(deltah2 * 1e3))                     
        return phimChoix
            

if __name__ == "__main__":
    import matplotlib.pylab as plt
    print("Test fbd")
    fck = 20. #MPa
    fyk = 500. #MPa
    phi = 25e-3
    condbet = "M"
    print("eta2(phi = {0:.0f}) = {1:.3f}".format(phi * 1e3, eta2(phi)))
    print("eta1(condbet) = {0:.3f}".format(eta11(condbet)))
    print("lbdrq = {:.3f} m".format(lbrqd1(condbet, phi, fck, MAT.fyd(fyk))))
    h = np.array([250, 300, 400, 400, 600, 600, 650, 650]) * 1e-3
    yi = np.array([200, 270, 200, 300, 200, 550, 200, 600]) * 1e-3
    for yk, hk in zip(yi, h):
        print("eta1(yi = {0:.3f}, h = {1:.3f}) = {2:.3f}".format(yk, hk, eta12(yk, hk)))
    plt.figure()
    plt.grid('on')
    x = np.linspace(0, 700e-3, 100)
    def f(h):
        if (h < 250e-3):
            return h
        if (h < 600e-3):
            return 250e-3
        else:
            return h - 300e-3
    y =np.array([f(xi) for xi in x])
    plt.plot(x * 1e3, y * 1e3, 'k')
    plt.plot(h * 1e3, yi * 1e3, 'k.')
    plt.plot([0, 700], [0, 700], 'k--')
    plt.xlabel("h [mm]")
    plt.ylabel("y [mm]")
    plt.savefig("./images/CondAdherence.pdf")
    print("Ancrage courbe")
    cnom = 30e-3
    FEd = 0.08
    ab = 46e-3
    fck = 25.
    condbet = "B"
    theta0 = 90. / 180. *pi
    lbd = 0.592
    t = 200e-3
    h = 460e-3
    phi, phit = 16e-3, 8e-3
    ancragecourbe(theta0, FEd, lbd, h, t, phi, phit, ab, cnom, fck, condbet, True)