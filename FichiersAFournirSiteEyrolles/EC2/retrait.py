#-*- coding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: retrait.py
"""
Module pour calculer les caractéristiques de retrait
"""
__version__ = '0.1'

import EC2.constantes as CST
from EC2.fluage import ho
from EC2.materiaux import fcm
from math import exp

def betadstts(Ac, u, t, ts):
    """    entree Ac : m², u: m, t: jours, ts:jours sortie : []
    """
    return max((t - ts) / (t - ts + 0.04 * ho(Ac, u)**(3. / 2.)), 0)
    
def kh(Ac, u):
    """tableau 3.3 approximation linéaire
    entree Ac : m², u: m sortie : []
    """
    hotmp = ho(Ac, u)
    kh100, kh200, kh300, kh500 = 1., 0.85, 0.75, 0.7
    h100, h200, h300, h500 = 100, 200, 300, 500
    if (hotmp < h100):
        return 1.
    elif (hotmp > h500):
        return 0.7
    elif (hotmp < h200):
        return kh100 + (kh200 - kh100) / (h200 - h100) * (hotmp - h100)
    elif (hotmp < h300):
        return kh200 + (kh300 - kh200) / (h300 - h200) * (hotmp - h200)
    elif (hotmp < h500):
        return kh300 + (kh500 - kh300) / (h500 - h300) * (hotmp - h300)

#def kh2(Ac, u):
#    """tableau 3.3 approximation parabolique
#    entree Ac : m², u: m sortie : []
#    """
#    hotmp = ho(Ac, u) #pas une bonne idée, parabole ne bas
#    if (hotmp > 500): #sinon parabole déborde....
#        return 0.7
#    else:
#        return min(1., max(1.2 - 2.25e-3 * hotmp +2.5e-6 * hotmp**2.0, 0.7))

def betaRH(RH):
    """coefficient annexe B.2
    en entrée : RH: % sortie :[]"""
    return 1.55 * (1.0 - (RH / 100.0)**3.0)


def epsiloncdO(typeCiment, fck, RH, aff = False):
    """déformation relative au retrait de desssication EpscdO
    entrée : typeciment: S,N,R fck: MPa, RH: % sortie :[]
    """
    fcmo = 10.
    if (typeCiment.upper() in CST.ALPHADSEC2):
        alphads1, alphads2 = CST.ALPHADSEC2[typeCiment.upper()]
    else:
        raise ValueError("Type de ciment uniquement : R, N, S")
    betaRH1 = betaRH(RH)
    epsiloncdO1 =  0.85 * ((220. + 110. * alphads1) * 
                           exp( - alphads2 * fcm(fck) / fcmo)) * betaRH1 * 1e-6
    if (aff):
        print("alphads1 = {:.3f} alphads2 = {:.3f}".format(alphads1, alphads2))
        print("fcm0 = {:.0f}) betaRH = {:.3f}".format(fcmo, betaRH1))
        print("epsiloncd0 = {:.3f} %".format(epsiloncdO1 * 1e2))
    return epsiloncdO1
    
def epsiloncd(Ac, u, typeCiment, fck, RH, aff = False):
    """retrait à l'infini
    entrée : Ac m2, u m, typeciment: S,N,R fck: MPa, RH: % sortie :[]
    """
    kh1 = kh(Ac, u) 
    if (aff):
        print("kh = {:.3f}".format(kh1))
    return kh1 * epsiloncdO(typeCiment, fck, RH, aff)

def epsiloncdt(t, ts, Ac, u, typeCiment, fck, RH, aff = False):
    """retrait au temps t
    """
    kh1 = kh(Ac, u) 
    betadstts1 = betadstts(Ac, u, t, ts)
    epsiloncdt1 = kh1 * epsiloncdO(typeCiment, fck, RH, aff) * betadstts1
    if (aff):
        print("kh = {:.3f}".format(kh1))
        print("beta(t = {:.1f}, ts = {:.1f}) = {:.3f}".format(t, ts, betadstts1))
        print("espsilon_cd(t = {:.1f}) = {:3f}".format(t, epsiloncdt1))
    return epsiloncdt1

##--------- RETRAIT ENDOGENE
def epsiloncainf(fck):
    """"
    entree fck: MPa sortie: []
    """
    return 2.5 * (fck - 10.) * 1e-6

def betaast(t):
    """entrée t:jours sortie: []
    """
    return 1. - exp(- 0.2 * t**(0.5))

def epsilonca(fck, aff = False):
    """retrait dessication à l'infini
    entrée, fck: MPa sortie, []
    """
    epsilonca1 =  epsiloncainf(fck)
    if (aff):
        print("epsilon_ca(t = infini) = {:3f} %".format(epsilonca1 * 1e2))
    return epsilonca1

def epsiloncat(t, fck, aff = False):
    """retrait endogene au temps t
    entrée t:jours, fck: MPa sortie: []
    """
    epsiloncainf1 = epsiloncainf(fck)
    betaast1 = betaast(t)
    epsiloncat1 =  epsiloncainf1 * betaast1
    if (aff):
        print("espilonca_inf = {:.3f} %".format(epsiloncainf1 * 1e2))
        print("betaast (t = {:.1f}) = {:.3f}".format(betaast1))
        print("epsiloncat = {:.3f} %".format(epsiloncat1 * 1e2))
    return epsiloncat1

##----- RETRAIT ENDOGENE + DESSICATION
def epsiloncs(Ac, u, typeCiment, fck, RH, aff = False):
    """"retrait total (endogene+dessication) au temps infini
    entrée Ac:m², u: m, typeCiment: S,N,R, fck: MPa, RH:%  sortie: []
    """
    return epsilonca(fck, aff) + epsiloncd(Ac, u, typeCiment, fck, RH, aff)

def epsiloncst(t, ts, Ac, u, typeCiment, fck, RH, aff = False):
    """retrait total (endogene+dessication) au temps t
    entrée t:j, ts:jours, Ac:m², u: m, typeCiment: S,N,R, fck: MPa, RH:%  sortie: []
    """
    return epsiloncat(t, fck, aff) + epsiloncdt(t, ts, Ac, u, typeCiment, fck, RH, aff)

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pylab as plt
    import EC2.fluage as EC2
    from EC2.materiaux import Ecm
    
    bw, h = 0.2, 0.4 #m, m, géométrie de la section rectangulaire
    Ac, u = bw * h, 2. * (bw + h) #aire, périmètre
    fck = 25. #MPa, résistance du béton
    RH = 70 #% pourcentage d'humidité relative
    t0 = 28.  #j, âge de chargement du béton
    sig0 = 20. #MPa, contrainte appliquée à t0 et constante quelque soit t
    typeCiment = "N" #classe du ciment
    ts = 5 #j, durée de la cure du béton
    
    t = np.linspace(0, 100., 100)
    Ec = 1.05 * Ecm(fck) #module sécant pour sig_c < 0.4 fck
    epscc = np.array([ sig0 / Ec * EC2.phitto(RH, Ac, u, fck, ti, t0, typeCiment) for ti in t])
    
    epscs = np.array([ epsiloncst(ti, ts, Ac, u, typeCiment, fck, RH) for ti in t])
    epsca = np.array([ epsiloncat(ti, fck) for ti in t])
    epscd = np.array([ epsiloncdt(ti, ts, Ac, u, typeCiment, fck, RH) for ti in t])
    #déformations de retrait : dessication & endogène
    plt.figure()
    plt.plot(t, epscs * 100, 'b-', label = r'$\epsilon_{cs}$')
    plt.plot(t, epsca * 100, 'r-', label = r'$\epsilon_{ca}$')
    plt.plot(t, epscd * 100, 'm-', label = r'$\epsilon_{cd}$')
    plt.grid(True)
    plt.xlabel(r't [j]')
    plt.legend(loc = 'best')
    plt.ylabel(r'$\epsilon$ [%]')
    plt.title(u'Déformation de retrait du béton')
    plt.savefig("./images/RetraitEpsT.pdf")
    #somme des déformations différées fluage & béton
    plt.figure()
    plt.plot(t, (epscs + epscc) * 100, 'b-', label = r'$\epsilon_{cs}+\epsilon_{cc}$')
    plt.grid(True)
    plt.xlabel(r't [j]')
    plt.legend(loc = 'best')
    plt.ylabel(r'$\epsilon_{c}$ [%]')
    plt.title(u'Déformation de fluage et de retrait du béton')
    plt.savefig("./images/RetraitFluageEpsT.pdf")
        