#-*- coding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: materiaux.py
"""
Module pour calculer les caractéristiques matériaux
"""
__version__ = '0.1'

import EC2.constantes as CST
from numpy import sign
from math import exp, log

def fcm(fck):
    """ résistance moyenne en compression à 28 jours 
        entrée : fck : MPa, sortie : fcm : MPa
    """
    if (fck <= CST.CMAX):
        return fck + 8.
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")
      

def fctm(fck):
    """résistance moyenne en traction à 28 jours 
    entrée fck : MPa, sortie : fctm : MPa
    """    
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 0.3 * fck**(2. / 3.)
        else:
            return 2.12 * log(1. + fcm(fck) / 10.)
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def fctk5(fck):
    """résistance moyenne en traction à 28 jours fractile 5%
    entrée fck : MPa, sortie : fctm : MPa
    """
    if (fck <= CST.CMAX):
        return 0.7 * fctm(fck)
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def fctk95(fck):
    """résistance moyenne en traction à 28 jours  fractile 95%
    entrée fck : MPa, sortie : fctm : MPa
    """
    if (fck <= CST.CMAX):
        return 1.3 * fctm(fck)
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def Ecm(fck): 
    """module moyen d'élasticité
    entrée fck : MPa, sortie : Ecm : MPa
    """
    if (fck <= CST.CMAX):
        return 22000. * (fcm(fck) / 10.)**0.3
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")


#déformation caractéristiques de la courbe Sigc/fcm=(kn-n²)/(1+(k-2)*n)
def epsilonc1(fck):
    """déformation au pic de la loi contrainte déformation du béton
        'entrée fck : MPa, sortie : epsilon : []
    """
    Udefo = 1e3 #passage sans unités
    if (fck <= CST.CMAX):
        return min(0.7 * (fcm(fck))**0.31, 2.8) / Udefo
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def epsiloncu1(fck):
    """déformation ultime de la loi contrainte déformation du béton en 
    parabole rectangle
    entrée fck : MPa, sortie : epsilon : []
    """
    Udefo = 1e3 #passage sans unités
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 3.5 / Udefo
        else:
            return (2.8 + 27.*((90 - fck) / 100.)**4)/ Udefo
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

#diagramme parabole rectangle
def epsilonc2(fck):
    """déformation à la fin de la parabole de la loi contrainte déformation 
    du béton en parabole rectangle
    'entrée fck : MPa, sortie : epsilon : []
    """
    Udefo = 1e3 #passage sans unités
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 2. / Udefo
        else:
            return (2.0 + 0.085 * (fck - 50.)**0.53) / Udefo
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def epsiloncu2(fck):
    """déformation à la fin de la parabole de la loi contrainte déformation 
    du béton en parabole rectangle
    'entrée fck : MPa, sortie : epsilon : []
    """
    Udefo = 1e3 #passage sans unités
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 3.5 / Udefo
        else:
            return (2.6 + 35. * ((90. - fck) / 100)**4) / Udefo
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

#diagramme bilinéaire
def epsilonc3(fck):
    """déformation à la fin de la parabole de la loi contrainte déformation du
    béton en parabole rectangle
    'entrée fck : MPa, sortie : epsilon : []
    """
    Udefo = 1e3 #passage sans unités
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 1.75 / Udefo
        else:
            return (1.75 + 0.55 * (fck - 50.) / 40.) / Udefo
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def epsiloncu3(fck):
    """déformation à la fin de la parabole de la loi contrainte déformation du
    béton en parabole rectangle
    'entrée fck : MPa, sortie : epsilon : []
    """
    Udefo = 1e3 #passage sans unités
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 3.5 / Udefo
        else:
            return (2.6 + 35. * ((90. - fck) / 100)**4) / Udefo
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

######################
def SigPar(eps, fck):
    """ A MODIFIER """
    print("OBSOLETE : prendre sigmac2")
    return sigmac2(eps, fck)

def SigPar2(eps, fck):
    """ A MODIFIER """
    print("OBSOLETE : prendre sigmac2b")
    return sigmac2b(eps, fck)

def sigsargin(eps, phi, fck):
    """ A MODIFIER """
    print("OBSOLETE : prendre sigmac1")
    return sigmac1(eps, fck)

def SigLin(eps, fck):
    """ A MODIFIER """
    print("OBSOLETE : prendre sigmac3")
    return sigmac3(eps, fck)

def sigs(epsS, fyk, k, epsuk):
    """ A MODIFIER """
    print("OBSOLETE : prendre sigmas2")
    return sigmas2(epsS, fyk, k, epsuk)

def sigs2(epsS, fyk):
    """ A MODIFIER """
    print("OBSOLETE : prendre sigmas1")
    return sigmas1(epsS, fyk)


######################
    
def sigmac1(eps, phi, fck):
    """loi pour les calculs au second ordre
    entrée : eps:[] phi, [] fck [MPa]
    sortie : [MPa]
    """
    epsc1 = - (1.0 + phi) * epsilonc1(fck)
    epscu1 = - (1.0 + phi) * epsiloncu1(fck)
    eta = abs(eps / epsc1)
    fcd1 = fcd(fck)
    if (eps > 0.0):
        return 0.0
    elif (eps > epscu1):
        k1 = 1.05 * Ecm(fck) * abs(epsc1) / CST.GAMMACE / fcd1
        return -fcd1 * (k1 * eta - eta**2.0) / (1.0 + (k1 - 2.0) * eta)
    else:
        return 0.0



def sigmac2(eps, fck):
    """fonction parabolique en fonction du coefficient puissance
    """
    if (eps >= 0):
        return 0  #pas de prise en compte de la traction
    elif (eps >= - epsilonc2(fck)):
        return -(1. - (1. + eps / epsilonc2(fck))**npuiss(fck)) * fcd(fck)
    elif (eps >= - epsiloncu2(fck)):
        return -fcd(fck)
    else:
        return 0.

def sigmac2b(eps, fck):
    """fonction parabolique en fonction du coefficient puissance
    """
    if (eps >= fctd(fck) / Ecm(fck)):
        return 0  #pas de prise en compte de la traction
    elif (eps >= 0):
        return Ecm(fck) * eps  #pas de prise en compte de la traction
    elif (eps >= -epsilonc2(fck)):
        return -(1. - (1. + eps / epsilonc2(fck))**npuiss(fck)) * fcd(fck)
    elif (eps >= -epsiloncu2(fck)):
        return -fcd(fck)
    else:
        return 0.

def sigmac3(eps, fck):
    """fonction bi linéaire variante 
    """
    if (eps >= 0):
        return 0  #pas de prise en compte de la traction
    elif (eps >= - epsilonc3(fck)):
        return -(- eps / epsilonc3(fck)) * fcd(fck)
    elif (eps >= - epsiloncu3(fck)):
        return -fcd(fck)
    else:
        return 0.


def npuiss(fck):
    """coefficient puissance de la "parabole"
    'entrée fck : MPa, sortie : []
    """
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 2.
        else:
            return 1.4 + 23.4 * ((90. - fck) / 100)**4.
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def alphae(fck):
    """coefficient d'équivalence
    'entree: fck:MPa, sortie:[]
    """
    if (fck <= CST.CMAX):
        return CST.ES / Ecm(fck)
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def sigmas1(eps, fyk):
    """valeur de la contrainte en un point quelconque du diagramme à palier horizontal
    'entrée : fyk: MPa, k: [], epsuk : [], eps : []
    """
    return sign(eps) * min(CST.ES * abs(eps), fyd(fyk))

def sigmas2(epsS, fyk, k, epsuk): 
    """valeur de la contrainte en un point quelconque du diagramme bilinéaire
    entrée : eps : [] fyk: MPa, k: [], epsuk : [],  sortie: [MPa]"""
    fyd1 = fyd(fyk)
    epse = fyd1 / CST.ES
    if (epsuk < epse): 
        raise ValueError("Données incohérentes Epsuk < Epse")
    if (abs(epsS) <= epse):     #domaine élastique
        return sign(epsS) * CST.ES * abs(epsS)
    else:     #domaine plastique
        if (abs(epsS) <= epsilonud(epsuk)):
            return sign(epsS) * fyd1 * (1. + (k - 1) * (abs(epsS) - epse) / (epsuk - epse))
        else:
            return 0.


#------------------- calcul section -------------------
def fcd(fck):
    """résistance en compression de dimensionnement
    'entrée fck : MPa, sortie : MPa
    """
    if (fck <= CST.CMAX):
        return CST.ALPHAC * fck / CST.GAMMAC
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def fctd(fck):
    """résistance en traction de dimensionnement
    'entrée fck : MPa, sortie : MPa
    """
    if (fck <= CST.CMAX):
           return CST.ALPHACT * fctk5(fck) / CST.GAMMAC
    else:    
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")
    
def fctml(fck, h):
    """résistance en flexion traction de dimensionnement
    'entrée fck : MPa, h : mm, sortie : MPa
    """
    if (fck <= CST.CMAX):
         return fctm(fck) * max((1.6 - h) / 1000., 1)
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")

def fyd(fyk):
    """"résistance en traction de dimensionnement
    'entrée fyk : MPa, sortie : MPa
    """
    return fyk / CST.GAMMAS


def epsilonud(epsilonuk):
    """déformation ultime résistance en traction de dimensionnement diagramme de calcul
    'entrée epsilonuk :[], sortie : []
    """
    return 0.9 * epsilonuk

def epsilone(fyk):
    """déformation élastique de l'acier 
    'entrée fyk:MPa, sortie : []
    """
    return fyd(fyk) / CST.ES

def lambdaR(fck):
    """hauteur relative du béton comprimé en flexion
    'entrée : fck: MPa, lambda:[]
    """
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 0.8
        else:
            return 0.8 - (fck - 50.) / 400.
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")
    
def eta(fck):
    """proportion de béton comprimé en flexion
    """
    if (fck <= CST.CMAX):
        if (fck <= 50):
            return 1.
        else:
            return 1.0 - (fck - 50.) / 200.
    else:
        raise ValueError("fck > C90/100 (EC2-3.1.2(2)P")
    

#------------------- fonction dépendant du temps --------------
def betacc(t, typeCiment, aff = False):
    """fonction de pondération afin de tenir compte de l'évolution du temps EN1992-1-1 3.1.2
    'entrée t : jours, s : [] sortie betacc : []
    """
    if (typeCiment.upper() in CST.SEC2):
        s = CST.SEC2[typeCiment.upper()]
    else:
        raise ValueError("Type de ciment uniquement : R, N, S")
    betacc1 = exp(s * (1. - (28. / t)**0.5))
    if (aff):
        print("s = {:.2f} pour du ciment {:s}".format(s, typeCiment.upper()))
        print("betacc = {:.3f}".format(betacc1))
    return betacc1

def fcmt(t, typeCiment, fck, aff = False):
    """contrainte moyenne en compression à t jours afin de tenir compte de l'évolution du temps EN1992-1-1 3.1.2
    'entrée t : jours, s : [], fck : MPa sortie fcmt : MPa
    """
    fcm1 = fcm(fck)
    fcmt1 = betacc(t, typeCiment, aff) * fcm1 
    if (aff):
        print("Résistance compression moyenne fcm = {:.3f} MPa".format(fcm1))
        print("Resistance compression moyenne fcm(t = {:.1f}) = {:.2f} MPa".format(fcmt1))
    return fcmt1


def fckt(t, typeCiment, fck, aff = False):
    """contrainte moyenne en compression à t jours afin de tenir compte de l'évolution du temps EN1992-1-1 3.1.2
    entrée t : jours, s : [], fcm : MPa sortie fcmt : MPa
    """
    if (t < 3.):
        raise ValueError("Essais complémentaires nécessaires")
    else:
        if (t < 28.):
            fckt1 = fcmt(t, typeCiment, fck, aff) - 8.
            if (aff):
                print("Résistance du béton fck(t = {:.1f}) = {:.2f} MPa".format(t, fckt1))
            return fckt1
        else:
            if (aff):
                print("Résistance du béton fck(t = {:.1f}) = {:.2f} MPa".format(t, fck))
            return fck

def fctmt(t, typeCiment, fck, aff = False):
    """'contrainte moyenne en traction à t jours afin de tenir compte de l'évolution du temps EN1992-1-1 3.1.2
    entrée t : jours, s : [], fck : MPa sortie fctmt : MPa
    """
    fctm1 = fctm(fck)
    if (t < 28.):
        fctmt1 = betacc(t,typeCiment, aff) * fctm1
        if (aff):
            print("Résistance traction moyenne fcm = {:.3f} MPa".format(fctm1))
            print("Resistance traction moyenne fcm(t = {:.1f}) = {:.2f} MPa".format(fctmt1))
        return fctmt1
    else:
        fctmt1 = betacc(t,typeCiment, aff)**(2./3.) * fctm1
        if (aff):
            print("Résistance traction moyenne fcm = {:.3f} MPa".format(fctm1))
            print("Resistance traction moyenne fcm(t = {:.1f}) = {:.2f} MPa".format(fctmt1))
        return fctm1
    
def Ecmt(t, typeCiment, fck, aff = False):
    """mdoule de déformation moyenne à t jours afin de tenir compte de l'évolution du temps EN1992-1-1 3.1.2
    entrée t : jours, typeCiment : [], fck : MPa sortie Ecmt : MPa
    """
    fcm1, Ecm1 = fcm(fck), Ecm(fck)
    Ecmt1 = (fcmt(t, typeCiment, fck, aff) / fcm1)**(0.3) * Ecm1
    if (aff):
        print("Résistance moyenne fcm = {:.3f} MPa".format(fcm1))
        print("Module sécant Ecm = {:.3f} MPa".format(Ecm1))
        print("Module sécant Ecm(t = {:.1f}) = {:.3f} MPa".format(Ecmt1))
    return Ecmt1

if __name__ == "__main__":
    #exemple1
    print("Test")
    fck = 30. #MPa
    print(u"Résistance caractéristique fck = {:.1f} MPa".format(fck))
    print(u"Résistance moyenne en compression fcm = {:.1f} MPa".format(fcm(fck)))
    help(fcm)
    #valeurs arrondies du tableau 3.1
    fck = CST.FCKEC2
    fcmR = [fcm(fcki) for fcki in fck]
    fctmR = [round(fctm(fcki), 1) for fcki in fck]
    fctk05R = [round(fctk5(fcki), 1) for fcki in fck]
    fctk95R = [round(fctk95(fcki), 1) for fcki in fck]
    EcmR= [round(Ecm(fcki) / 1000, 0) for fcki in fck]
    epsc1R = [round(epsilonc1(fcki) * 1e3, 1) for fcki in fck]
    epscu1R = [round(epsiloncu1(fcki) * 1e3, 1) for fcki in fck]
    epsc2R = [round(epsilonc2(fcki) * 1e3, 1) for fcki in fck]
    epscu2R = [round(epsiloncu2(fcki) * 1e3, 1) for fcki in fck]
    nR = [round(npuiss(fcki), 1) for fcki in fck]
    epsc3R = [round(epsilonc3(fcki) * 1e3, 1) for fcki in fck]
    epscu3R = [round(epsiloncu3(fcki) * 1e3, 1) for fcki in fck]
    #utilisation de la loi parabole rectangle
    import matplotlib.pylab as plt
    import numpy as np
    #parmétrage initial
    fck = 30.
    epscu2 = - epsiloncu2(fck)
    #tracé de la loi de comportement contrainte déformations béton
    plt.figure()
    X = np.linspace( epscu2 - 0.0001, 0.0001 , 100)
    Y = np.array([ sigmac2(Xi, fck) for Xi in X ])
    plt.plot( X * 100, Y, 'k-')
    plt.grid(True)
    plt.xlabel(r'$\epsilon$ [%]')
    plt.ylabel(r'$\sigma$ [MPa]')
    plt.title(u'Loi de comportement béton parabole rectangle')
    plt.savefig("./images/CourbeSigDef.pdf")
    plt.show() 

