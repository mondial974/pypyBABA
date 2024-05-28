#!/usr/bin/python
#-*- coding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: fluage.py
"""
Module pour calculer les caractéristiques de fluage
"""
__version__ = '0.1'

import EC2.constantes as CST
from EC2.materiaux import fcm
from math import exp

def ho(Ac, u):    
    """entrée Ac: m², u: m, sortie: ho:mm
    """
    if (abs(u) > CST.ZERO):
        return 2. * Ac / u * 1000. #attention en mm pour les formules
    else:
        raise ValueError("périmètre u nul")

def betaH(RH, Ac, u, fck, aff = False):
    """entrée RH : %, Ac: m², u: m, fck: MPa, to: jours
    """
    fcm1 = fcm(fck)
    alpha3 = (35. / fcm1)**0.5
    ho1 = ho(Ac, u)
    if (fcm1 <= 35):
        betaH1 = min(1.5 * (1. + (0.012 * RH)**18) * ho(Ac, u) + 250., 1500.)
        if (aff):
            print("fcm = {:.2f} MPa < 35 MPa".format(fcm1))
            print("ho =  {:.2f} mm, alpha3 = {:.3f}".format(ho1, alpha3))
            print("betaH = {:.3f}".format(betaH1))
        return betaH1 
    else:
        betaH1 = min(1.5 * (1. + (0.012 * RH)**18) * ho(Ac, u) + 250. * alpha3, 1500. * alpha3)
        if (aff):
            print("fcm = {:.2f} MPa > 35 MPa".format(fcm1))
            print("ho =  {:.2f} mm, alpha3 = {:.3f}".format(ho1, alpha3))
            print("betaH = {:.3f}".format(betaH1))
        return betaH1 

def betactto(RH, Ac, u, fck, t, to, typeCiment, aff = False):
    """entrée RH : %, Ac: m², u: m, fck: MPa, to: jours, typeCiment : S, N, R
    """
    if (t < to):
       return 0.0
    else:
        betactto1 = ((t - to)/(betaH(RH, Ac, u, fck, aff) + t - to))**(0.3)
        if (aff):
            print("betactto( t = {:.1f}, to = {:.1f}) = {:.3f}".format(t, to, betactto1))
        return betactto1

def phiRH(RH, Ac, u, fck, aff = False):
    """influence de l'humidité relative RH
    entrée RH : %, Ac: m², u: m, fck: MPa
    """
    fcm1 = fcm(fck)
    ho1 = ho(Ac, u)
    if (fcm1 <= 35):
        phiRH1 = 1. + (1. - RH / 100.)/(0.1 * (ho1)**(1. / 3.))
        if (aff):
            print("fcm = {:.2f} MPa < 35 MPa".format(fcm1))
            print("phiRH = {:.3f}".format(phiRH1))
        return phiRH1
    else:
        alpha1 = (35. / fcm1)**0.7
        alpha2 = (35. / fcm1)**0.2
        phiRH1 = (1. + (1. - RH / 100.)/(0.1 * (ho1)**(1. / 3.))* alpha1) * alpha2
        if (aff):
            print("fcm = {:.2f} MPa > 35 MPa".format(fcm1))
            print("alpha1 = {:3f} alpha2 = {:.3f}".format(alpha1, alpha2))
            print("phiRH = {:.3f}".format(phiRH1))
        return phiRH1


def betafcm(fck, aff = False):
    """annexe B : entrée fck: MPa
    """
    betafcm1 = 16.8 / (fcm(fck))**(0.5)
    if (aff):
        print("betafcm = {:.3f}".format(betafcm1))
    return betafcm1

def betato(to, typeCiment, aff = False, To = 20.):
    """annexe B
    """
    to = ageciment(to, typeCiment, aff, To)
    betato1 = 1./ (0.1 + to**(0.2))
    if (aff):
        print("to = {:.2f} j".format(to))
        print("betato = {:3f}".format(betato1))
    return betato1

def phi0(RH, Ac, u, fck, to, typeCiment, aff= False, To = 20.):
    """entrée RH : %, Ac: m², u: m, fck: MPa, tto: jours, To : °C
    """
    return phiRH(RH, Ac, u, fck, aff) * betafcm(fck, aff) * betato(to, typeCiment, aff, To)

def ageciment(to, typeCiment, aff = False, To = 20):
    """alpha : []
    """
    if (typeCiment.upper() in CST.ALPHAEC2):
        alpha = CST.ALPHAEC2[typeCiment.upper()]
    else:
        raise ValueError("Type de ciment uniquement : R, N, S")
    toT = dureeti(to, To) #pas de sommation 
    ageciment1 = max(toT*(9. / (2. + toT**(1.2)) + 1.)**alpha, 0.5)
    if (aff):
        print("alpha = {:.2f}".format(alpha))
        print("toT = {:.2f} j, attention hypothèse à 20°".format(toT))
        print("age du ciment {:.2f} j".format(ageciment1))
    return ageciment1

def dureeti(Dti, Ti):
    """Ti: °C, Dti : jours
    """
    return exp(-(4000. / ( 273. + Ti) - 13.65)) * Dti

def phitto(RH, Ac, u, fck, t, to, typeCiment, aff = False, To = 20.):
    """fonction de fluage entre t et to
    entrée RH : %, Ac: m², u: m, fck: MPa, t,to: jours, typeCiment : S,N,R
    """
    betac = betactto(RH, Ac, u, fck, t, to, typeCiment, aff)
    #to = ageciment(typeCiment, to, To) #on modifie l'age du ciment
    phiinf1 = phi0(RH, Ac, u, fck, to, typeCiment, aff, To) * betac
    if (aff):
        print(u"Coefficient de fluage phi(t = {:.1f}, to = {:.1f}) = {0:.3f}".format(t, to, phiinf1))
    return phiinf1

def phiinfto(RH, Ac, u, fck, to, typeCiment, aff = False, To = 20.):
    """fonction de fluage entre to et l'infini
    entrée RH : %, Ac: m², u: m, fck: MPa, to: jours, typeCiment : S,N,R
    """
    betac = 1.
    #tto = ageciment(typeCiment, to) #on modifie l'age du ciment
    phiinf1 = phi0(RH, Ac, u, fck, to, typeCiment, aff, To) * betac
    if (aff):
        print(u"Coefficient de fluage à l'infini phi = {0:.3f}".format(phiinf1))
    return phiinf1

if __name__ == "__main__":
    bw, h = 0.2, 0.4 #m, m, géométrie de la section rectangulaire
    Ac, u = bw * h, 2. * (bw + h) #aire, périmètre
    fck = 25. #MPa, résistance du béton
    RH = 70 #% pourcentage d'humidité relative
    t0 = 28.  #j, âge de chargement du béton
    typeCiment = "N" #classe du ciment
    phiinf = phiinfto(RH, Ac, u, fck, t0, typeCiment, True)
    #fluage à l'infini
    import numpy as np
    import matplotlib.pylab as plt
    sig0 = 20. #MPa, contrainte appliquée à t0 et constante quelque soit t
    t = np.linspace(0, 100., 100)
    Ec = 1.05 * Ecm(fck) #module sécant pour sig_c < 0.4 fck
    epsc = np.array([ sig0 / Ec * phitto(RH, Ac, u, fck, ti, t0, typeCiment) for ti in t])
    #tracé de la loi de comportement contrainte déformations béton
    plt.figure()
    plt.plot(t, epsc * 100, 'b-')
    plt.grid(True)
    plt.xlabel(r't [j]')
    plt.ylabel(r'$\epsilon$ [%]')
    plt.title(u'Déformation de fluage du béton')
    plt.savefig("./FluageEps.pdf")
    