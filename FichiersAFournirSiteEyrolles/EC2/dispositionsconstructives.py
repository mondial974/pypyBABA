#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: dispositionsconsrtructives.py
"""
Module pour calculer les dispositions constructives
"""
__version__ = '0.1'

import EC2.constantes as CST
import EC2.materiaux as MAT
from math import pi, ceil
from scipy.optimize import fsolve
import numpy as np


def HA(n, diam):
    """ aire de n diamètre
    entrée : n[], diam [mm] sortie m2"""
    return float(n) * pi * (float(diam) * 1e-3)**2.0 / 4.0


def ST(ref, aff = False):
    """ renvoie la section d'un treillis soudé
    entrée : ref[str], sortie As [mm²] """
    ###S : s : E : e : D : d : AV : AR : N : n : L : l
    ts = {      "ST15C"  : [142e-6, 142e-6, 200e-3, 200e-3, 6e-3, 6e-3, 100e-3, 100e-3, 100e-3, 100e-3, 12, 20, 4.,2.4 ],
                "ST20"   : [189e-6, 128e-6, 150e-3, 300e-3, 6e-3, 7e-3, 150e-3, 150e-3, 75e-3, 75e-3, 16, 20, 6, 2.4 ],
                "ST25"   : [257e-6, 128e-6, 150e-3, 300e-3, 7e-3, 7e-3, 150e-3, 150e-3, 75e-3, 75e-3, 16, 20, 6, 2.4 ],
                "ST25C"  : [157e-6, 257e-6, 150e-3, 150e-3, 7e-3, 7e-3, 75e-3, 75e-3, 75e-3, 75e-3, 16, 40, 6, 2.4 ],
                "ST25CS" : [157e-6, 257e-6, 150e-3, 150e-3, 7e-3, 7e-3, 75e-3, 75e-3, 75e-3, 75e-3, 16, 20, 3, 2.4 ],
                "ST35"   : [385e-6, 128e-6, 100e-3, 300e-3, 7e-3, 7e-3, 150e-3, 150e-3, 50e-3, 50e-3, 24, 40, 6, 2.4 ],
                "ST40C"  : [385e-6, 385e-6, 100e-3, 100e-3, 7e-3, 7e-3, 50e-3, 50e-3, 50e-3, 50e-3, 24, 60, 6, 2.4 ],
                "ST50"   : [503e-6, 168e-6, 100e-3, 300e-3, 8e-3, 8e-3, 150e-3, 150e-3, 50e-3, 50e-3, 24, 40, 6, 2.4 ],
                "ST50C"  : [503e-6, 503e-6, 100e-3, 100e-3, 8e-3, 8e-3, 50e-3, 50e-3, 50e-3, 50e-3, 24, 40, 6, 2.4 ],
                "ST60"   : [636e-6, 254e-6, 100e-3, 250e-3, 9e-3, 9e-3, 125e-3, 125e-3, 50e-3, 50e-3, 24, 24, 6, 2.4 ],
                "ST65C"  : [636e-6, 636e-6, 100e-3, 100e-3, 9e-3, 9e-3, 50e-3, 50e-3, 50e-3, 50e-3, 24, 60, 6., 2.4 ],
                "PAFR"   : [80e-6, 53e-6, 200e-3, 300e-3, 4.5e-3, 4.5e-3, 150e-3, 150e-3, 100e-3, 100e-3, 12, 12, 3.6, 2.4],
                "PAFC"   : [80e-6, 80e-6, 200e-3, 200e-3, 4.5e-3, 4.5e-3 ,100e-3, 100e-3, 100e-3, 100e-3, 12, 18 ,3.6, 2.4],
                "PAFV"   : [80e-6, 99e-6, 200e-3, 160e-3 ,4.5e-3, 4.5e-3, 135e-3, 25e-3, 100e-3, 100e-3, 12, 16, 3.2, 2.4],
                "PAF10"  : [119e-6, 119e-6, 200e-3, 200e-3, 5.5e-3, 5.5e-3, 100e-3, 100e-3 ,100e-3 ,100e-3, 12, 21, 4.2, 2.4]              
                }                
    if (not (ref in ts)): 
        s = ""
        for cle in ts.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))  
        raise ValueError("Cle absente pour REF = {0:s}".format(ref))
        return 0.
    if (aff):
        print("Treillis soudes {0:s}".format(ref))
        print(" Sections  S = {0:.0f} mm², s = {1:.0f}  mm²".format(ts[ref][0] * 1e6, ts[ref][1] * 1e6))
        print(" Mailles   E = {0:.0f} mm,  e = {1:.0f}  mm".format(ts[ref][2] * 1e3, ts[ref][3] * 1e3))
        print(" Diamètres D = {0:.0f} mm,  s = {1:.0f}  mm".format(ts[ref][4] * 1e3, ts[ref][5] * 1e3))
        print(" Abouts   AV = {0:.0f} mm, AR = {1:.0f}  mm".format(ts[ref][6] * 1e3,  ts[ref][7] * 1e3))
        print(" Abouts   ad = {0:.0f} mm, ag = {1:.0f}  mm".format(ts[ref][8] * 1e3, ts[ref][9] * 1e3))
        print(" Nb fils   N = {0:.0f}   , n = {1:.0f}".format(ts[ref][10] , ts[ref][11] ))
        print(" Longueur  L = {0:.1f} m,  l = {1:.1f}  m".format(ts[ref][12], ts[ref][13]))      
    return ts[ref]

############################
### Gestion du paquet de barres
###########################

def CDG_acier1file(phi, cnom, phit):
    """ centre de gravité d'une file d'armatures
    entrée : phi, cnom, phit [m], sortie : [m]"""
    phi = np.array(phi)
    if (len(phit) > 3):
        raise ValueError("Taille du paquet supérieur à 3")
    ygj = [cnom + phit + sum([phi[k] for k in range(j)]) \
           + phi[j] /2 for j in range(len(phi))]
    phi2 = phi * phi
    yg1 = 0
    for ygi, phi2j in zip(ygj, phi2):
        yg1 += ygi * phi2j
    return yg1 / np.sum(phi2)

def CDG_acier3lits(phi, cnom, phit):
    """ centre de gravité d'un paquet d'armatures valable pour 3 lits 
    entrée : phi, cnom, phit [m], sortie : [m]"""
    if (len(phi) > 3):
        raise ValueError("Nombre de lits trop grand")
    phi = np.array(phi)
    phi2 = phi * phi
    Sphi2 = sum(sum(phi2))
    ygj = [cnom + phit + sum([phi[k] for k in range(j)]) \
           + phi[j] / 2. for j in range(len(phi))]
    Sstat = sum(sum(ygj * phi2))
    yg = Sstat / Sphi2
    return yg


def CDG_aciernlits2(phi, dg, cnom, phit, bw, ygj = []):
    """ centre de gravité d'un paquet d'armatures valables pour n lits 
    on suppose que l'on empile au maximum...
    entrée : phi, cnom, phit [m], sortie : [m]"""
    if (len(ygj) != 0):
        phi = np.array(phi)
        phi2 = phi * phi
        Sphi2 = sum(sum(phi2))
        Sstat = sum(sum(ygj * phi2))
        yg = Sstat / Sphi2
        return yg
    if (len(phi) <= CST.NB): 
        phi = np.array(phi)
        phi2 = phi * phi
        phiiphij = np.max( phi / np.min(phi, axis = 0))
        if (phiiphij > CST.PHIIPHIJ):
            raise ValueError("Rapport de diametre > {}".format(CST.PHIIPHIJ))
        phintemp = max(sum(phi2)**0.5)
        if (phintemp > CST.PHINMAX):
            raise ValueError("Diametre trop important dans le paquet")
        Sphi2 = sum(sum(phi2))
        ygj = [cnom + phit + sum([phi[k] for k in range(j)]) \
               + phi[j] / 2. for j in range(len(phi))]
        Sstat = sum(sum(ygj * phi2))
        yg = Sstat / Sphi2
        return yg
    else: #paquets de barres supérieures à NB = 3
        phin = 0.
        for i in range(int(ceil(len(phi) / float(CST.NB)))):
            idmin, idmax = int(CST.NB) * i, min(int(CST.NB) * (i + 1), len(phi))
            phitemp = phi[idmin:idmax]
            phiiphij = np.max( phitemp / np.min(phitemp, axis = 0))
            if (phiiphij > CST.PHIIPHIJ):
                raise ValueError("Rapport de diametre > {}".format(CST.PHIIPHIJ))
            phintemp = max(sum(phitemp * phitemp)**0.5)
            if (phintemp > CST.PHINMAX):
                raise ValueError("Diametre trop important dans le paquet")
            phin = max(phin, phintemp)        
        print("phi_n = {0:.3f} mm".format(phin * 1e3))
        phimax = np.max(phi, axis = 0)
        eh = (bw - (2 * cnom + 2 * phit + sum(phimax))) / (len(phimax) - 1)
        print("eh = {0:.3f} mm".format(eh * 1e3))
        ehmax = max(CST.K1PHI * phin, dg + CST.K2DG, CST.EHMIN)
        print("ehmax = {0:.3f} mm".format(ehmax * 1e3))
        if (eh < ehmax):
            raise ValueError("Espacment trop reduit eh {} < ehmax {}".format(eh, ehmax))        
        ygj = [cnom + phit + sum([phi[k] for k in range(j)]) \
               + phi[j] / 2. + int(j / float(CST.NB)) * ehmax for j in range(len(phi))]
        phi2 = phi * phi
        Sphi2 = sum(sum(phi2))
        Sstat = sum(sum(ygj * phi2))
        yg = Sstat / Sphi2
        return yg
        
def CDG_aciernlits(phi, dg, cnom, phit, bw, aff = False, ygj = []):
    """ centre de gravité d'un paquet d'armatures valables pour n lits 
    on suppose que l'on empile au maximum...
    entrée : phi, cnom, phit [m], sortie : [m]"""
    if (len(ygj) != 0):
        phi = np.array(phi)
        phi2 = phi * phi
        Sphi2 = sum(sum(phi2))
        Sstat = sum(sum(ygj * phi2))
        yg = Sstat / Sphi2
        return yg
    phin = 0.
    for i in range(int(ceil(len(phi) / float(CST.NB)))):
        idmin, idmax = int(CST.NB) * i, min(int(CST.NB) * (i + 1), len(phi))
        phitemp = phi[idmin:idmax]
        phiiphij = np.max( phitemp / np.min(phitemp[phitemp != 0], axis = 0))
        if (phiiphij > CST.PHIIPHIJ):
            raise ValueError("Rapport de diametre > {}".format(CST.PHIIPHIJ))
        phintemp = max(sum(phitemp * phitemp)**0.5)
        if (phintemp > CST.PHINMAX):
            raise ValueError("Diametre trop important dans le paquet")
        phin = max(phin, phintemp)        
    if (aff): print("phi_n = {0:.3f} mm".format(phin * 1e3))
    phimax = np.max(phi, axis = 0)
    eh = (bw - (2 * cnom + 2 * phit + sum(phimax))) / (len(phimax) - 1)
    if (aff): print("eh = {0:.3f} mm".format(eh * 1e3))
    ehmin = max(CST.K1PHI * phin, dg + CST.K2DG, CST.EHMIN)
    if (aff): print("ehmin = {0:.3f} mm".format(ehmin * 1e3))
    if (eh < ehmin):
        raise ValueError("Espacement trop reduit eh {} < ehmin {}".format(eh, ehmin))        
    ygj = [cnom + phit + sum([phi[k] for k in range(j)]) \
           + phi[j] / 2. + int(j / float(CST.NB)) * ehmin for j in range(len(phi))]
    phi2 = phi * phi
    Sphi2 = sum(sum(phi2))
    Sstat = sum(sum(ygj * phi2))
    yg = Sstat / Sphi2
    return yg


##### Enrobage et durabilité
def eh(phi, phit, bw, cnom):
    """ espacement horizontal entre les paquets barres
    entrée : phi, bw, cnom [m], sortie : [m]"""
    phimax = np.max(phi, axis = 0)
    eh1 = (bw - (2 * cnom + 2 * phit + sum(phimax))) / (len(phimax) - 1)
    return eh1

def ev(phi, phit, bw, cnom):
    """ espacement vertical entre les paquets de barres
    entrée : phi, bw, cnom [m], sortie : [m]"""
    phimax = np.max(phi, axis = 0)
    ev1 = (bw - (2 * cnom + 2 * phit + sum(phimax))) / (len(phimax) - 1)
    return ev1

def ehmax(phi, dg):
    phin1 = phin(phi)
    ehmax = max(CST.K1PHI * phin1, dg + CST.K2DG, CST.EHMIN)
    return ehmax

def phin(phi):
    """ diamètre équivalent du paquet de barres
    entrée phi:[m] sortie: [m]    """
    phin = 0.
    for i in range(int(ceil(len(phi) / float(CST.NB)))):
        idmin, idmax = int(CST.NB) * i, min(int(CST.NB) * (i + 1), len(phi))
        phitemp = phi[idmin:idmax]
        phiiphij = np.max( phitemp / np.min(phitemp[phitemp != 0], axis = 0))
        if (phiiphij > CST.PHIIPHIJ):
            raise ValueError("Rapport de diametre > {}".format(CST.PHIIPHIJ))
        phintemp = max(sum(phitemp * phitemp)**0.5)
        if (phintemp > CST.PHINMAX):
            raise ValueError("Diametre trop important dans le paquet")
        phin = max(phin, phintemp) 
    return phin

def fckmindur(ref, aff = False):
    """ résistance minimale pour la durabilité, indicaditif, annexe E
    entrée : ref:[] sortie: [[], MPa]"""
    fckmin1 = 0.
    for refi in refs.split(" "):
        if (refi[:3] in CST.FCKMINIDUR.keys()): #classes initiales
            fckmindur1 = CST.FCKMINIDUR[refi[:3]]
            if (fckmindur1 > fckmin1): #on mémorise
                fckmin1, refmax = fckmindur1, refi
        else:#clé absente, soucis
            s = ""
            for cle in CST.FCKMINIDUR.keys():
                s += cle + " "
            print("Clés utilisables : {0:s}".format(s))
            raise ValueError("Cle absente pour REF = {0:s}".format(refi))   
    if (aff): 
        print("Classe dimensionnante : {:s} - fck = {:.0f} MPa".format(refmax, fckmin1))
    return [refmax, fckmin1]


def cmindurBA(ref, classe, aff = False):
    """ enrobage de durabilité 
    entrée: ref [], classe [], sortie: [m]
    ref : XF1pf XF2f, XF2fexp XF3pf XF3pfee XF4f XF4fexp XF4tf
        : X0 XC1..4 XD1..3 XS1..3
        pf : peu fréquent, f : frequent, tf: très fréquent
        exp: exposé, ee: avec entraineur d'air cf AN 4.2(2)"""
    if (classe < CST.CLASSESTRUCTMIN) and  (classe > CST.CLASSESTRUCTMAX):
        raise ValueError("La classe internationale doit entre comprise entre {:.0f} et {:.0f}"
                         .format(CST.CLASSESTRUCTMIN, CST.CLASSESTRUCTMAX))
    if (ref in CST.CMINDURBA1.keys()): #classes initiales
        cmindur1 = CST.CMINDURBA1[ref][classe] * 1e-3
        if (aff): 
            print("Classe : {:s} - cmin,dur = {:.0f} mm".format(ref, cmindur1 * 1e3))
        return cmindur1
    if (ref in CST.CMINDURBA2.keys()): #classes par équivalence
        cmindur2 = CST.CMINDURBA2[ref][classe] * 1e-3
        if (aff): 
            print("Classe : {:s} - cmin,dur = {:.0f} mm".format(ref, cmindur2 * 1e3))
        return cmindur2
    s = ""
    for cle in CST.CMINDURBA1.keys():
        s += cle + " "
    for cle in CST.CMINDURBA2.keys():
        s += cle + " "
    print("Clés utilisables : {0:s}".format(s))
    raise ValueError("Cle absente pour REF = {0:s}".format(ref))

def cmindurBA2(refs, classe, aff = False):
    """ calcul de l'enrobage pour n classes d'environnement "XS1 XD3"
    entrée: ref [], classe [], sortie: [[], m]"""
    cmin1 = 0.
    for refi in refs.split(" "):
        cmini = cmindurBA(refi, classe, aff)
        if (cmini >= cmin1):
            refmax, cmin1 = refi, cmini
    if (aff):
        print("Classe maximale retenue : {:s} - cmin,dur = {:.0f} mm"
              .format(refmax, cmin1 * 1e3))
    return [refmax, cmin1]

def cminXM(ref, aff = False):
    """complément d'enrobage lié à l'attrition 4.4.1.2(13)
    entrée: classe [], sortie [m]"""
    if (ref in CST.KXM.keys()): #classes initiales
        cmindur1 = CST.KXM[ref] * 1e-3
        if (aff): 
            print("Classe : {:s} - cmin + {:.0f} mm (<- à ajouter)".format(ref, cmindur1 * 1e3))
        return cmindur1
    else:
        s = ""
        for cle in CST.KXM.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour REF = {0:s}".format(ref))
        
def corr_classe_enrob(ref, classe, aff = False):
    """ correction de la classe structurale en fonction de l'enrobage
    entrée : ref, classe [], sortie: []"""
    if (classe < CST.CLASSESTRUCTMIN) and  (classe > CST.CLASSESTRUCTMAX):
        raise ValueError("La classe internationale doit entre comprise entre {:.0f} et {:.0f}"
                         .format(CST.CLASSESTRUCTMIN, CST.CLASSESTRUCTMAX))
    if (ref in CST.ENRCOMP.keys()): #classes initiales
        Dclasse = CST.ENRCOMP[ref]
        classe_corr = min(max(classe + Dclasse, CST.CLASSESTRUCTMIN),
                     CST.CLASSESTRUCTMAX)
        if (aff): 
            print("Enrobage compactage en classe {:s} : S{:.0f} -> S{:.0f}".format(ref, classe, classe_corr))
        return classe_corr
    else:
        s = ""
        for cle in CST.ENRCOMP.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour REF = {0:s}".format(ref))
   
def corr_classe_duree100(ref, classe, aff = False):
    """ correction de la classe structurale en fonction de la durée du projet
    entrée : ref, classe [], sortie: []"""
    if (classe < CST.CLASSESTRUCTMIN) and  (classe > CST.CLASSESTRUCTMAX):
        raise ValueError("La classe internationale doit entre comprise entre {:.0f} et {:.0f}"
                         .format(CST.CLASSESTRUCTMIN, CST.CLASSESTRUCTMAX))
    if (ref in CST.DUREE100.keys()): #classes initiales
        Dclasse = CST.DUREE100[ref]
        classe_corr = min(max(classe + Dclasse, CST.CLASSESTRUCTMIN),
                     CST.CLASSESTRUCTMAX)
        if (aff): 
            print("Durée de projet supérieure à 100 ans en classe {:s} : S{:.0f} -> S{:.0f}".format(ref, classe, classe_corr))
        return classe_corr
    else:
        s = ""
        for cle in CST.DUREE100.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour REF = {0:s}".format(ref))

def corr_classe_duree25(ref, classe, aff = False):
    """ correction de la classe structurale en fonction de la durée du projet
    entrée : ref, classe [], sortie: []"""
    if (classe < CST.CLASSESTRUCTMIN) and  (classe > CST.CLASSESTRUCTMAX):
        raise ValueError("La classe internationale doit entre comprise entre {:.0f} et {:.0f}"
                         .format(CST.CLASSESTRUCTMIN, CST.CLASSESTRUCTMAX))
    if (ref in CST.DUREE25.keys()): #classes initiales
        Dclasse = CST.DUREE25[ref]
        classe_corr = min(max(classe + Dclasse, CST.CLASSESTRUCTMIN),
                     CST.CLASSESTRUCTMAX)
        if (aff): 
            print("Durée de projet inférieure à 25 ans en classe {:s} : S{:.0f} -> S{:.0f}".format(ref, classe, classe_corr))
        return classe_corr
    else:
        s = ""
        for cle in CST.DUREE25.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour REF = {0:s}".format(ref))

def corr_classe_resist(ref, classe, fck, aff = False):
    """ correction de la classe structurale en fonction de la durée du projet
    entrée : ref, classe [], sortie: []"""
    if (classe < CST.CLASSESTRUCTMIN) and  (classe > CST.CLASSESTRUCTMAX):
        raise ValueError("La classe internationale doit entre comprise entre {:.0f} et {:.0f}"
                         .format(CST.CLASSESTRUCTMIN, CST.CLASSESTRUCTMAX))
    if (fck < 0.) or (not fck in CST.FCKEC2):
        print("Résistance standard autorisée : {:s} MPa".format(str(CST.FCKEC2)))
        raise ValueError("fck non standard")
    if (ref in CST.CLASSRESIST.keys()): #classes initiales
        donnee = CST.CLASSRESIST[ref]
        if (fck >= donnee[1][0]):
            Dclasse = donnee[1][1]
            classe_corr = min(max(classe + Dclasse, CST.CLASSESTRUCTMIN),
                     CST.CLASSESTRUCTMAX)
            if (aff): 
                print("fck = {:.0f} > {:.0f} MPa en classe {:s} : S{:.0f} -> S{:.0f}"
                      .format(fck, donnee[1][0],ref, classe, classe_corr))
            return classe_corr
        elif (fck >= donnee[1][0]) and (fck < donnee[1][0]):
            Dclasse = donnee[0][1]
            classe_corr = min(max(classe + Dclasse, CST.CLASSESTRUCTMIN),
                     CST.CLASSESTRUCTMAX)
            if (aff): 
                print("fck = {:.0f} > {:.0f} MPa et < {:.0f} MPa en classe {:s} : S{:.0f} -> S{:.0f}"
                      .format(fck, donnee[0][0], donnee[1][0],ref, classe, classe_corr))
            return classe_corr
        else:
            print("Pas de modulation pour fck = {:.0f} MPa en classe {:s} : S{:.0f}"
                  .format(fck, ref, classe))
            return classe
    else:
        s = ""
        for cle in CST.CLASSRESIST.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour REF = {0:s}".format(ref))
   
def corr_classe_modulation(ref, duree, fck, enrcompact = False, aff = False):
    """ modulation de la classe de résistance en fonction des données d'entrée
    entrée: ref, classe [], duree [an], fck [MPa], enrcompact [], sortie: []"""
    classe = CST.CLASSESTRUCTDEF
    if (duree <= CST.DUREEMIN):
        classe = corr_classe_duree25(ref, classe, aff)
    if (duree >= CST.DUREEMAJ):
        classe = corr_classe_duree100(ref, classe, aff)
    if (enrcompact):
        classe = corr_classe_enrob(ref, classe, aff)
    classe = corr_classe_resist(ref, classe, fck, aff)
    if (aff):
        print("Soit au final une classe structurale S{:.0f}".format(classe))
    return classe

def cnomBA(phi, ref, classe, dg, aff = False, XM = "", DcDev = CST.DCDEV):
    """ enrobage nominale entre le paquet de barre
    entrée : phi:[mm], ref, classe, sortie:[m]"""
    cminb = phin(phi)
    cmindur = cmindurBA(ref, classe, aff)
    cnom1 = max (cminb, cmindur, CST.CMIN) + DcDev
    if (XM != ""):
        cnom1 += cminXM(XM, aff)
    if (dg > CST.DGDIFF):
        cnom1 += CST.CMINDG
        if (aff):
            print("dg = {:.3f} mm > {:.0f} mm : majoration de {:.0f} mm"
                  .format(dg * 1e3, CST.DGDIFF * 1e3, CST.CMINDG * 1e3))
    cnom1 = ceil( cnom1 / 5e-3) * 5e-3 #arrondi par pas de 5mm
    if (aff): 
        print("Enrobage nominale : cnom = {:.0f} mm".format(cnom1 * 1e3))
    return cnom1 

def yHA(yGi, phii, h):
    """ type d'adhérence (bonne/mauvaise) en fonction de l'altitude 
    de la barre dans la poutre de hauteur h
    entrée : yGi, phii, h [m], sortie : [Bonne/Mauvaise]"""
    def type_adherence(y, h):
        """fonction locale permettant de tester la position 
        entrée: y, h [m], sortie : [True/False]"""
        if (h < .250):
            return True
        elif (h < .600):
            if (y < .250):
                return True
            else:
                return False
        else:
            if (y < h - .300):
                return True
            else:
                return False
    if (yGi - phii / 2. < 0) or (yGi + phii / 2. > h):
        raise ValueError("Probleme d'enrobage")
    res1 = type_adherence(yGi - phii / 2., h)
    res2 = type_adherence(yGi + phii / 2., h)
    if (res1 & res2):
        return "Bonne"
    else: 
        return "Mauvaise"

if __name__ == "__main__":
    print("Test HA")
    As = HA(3, 32)
    print("As(3HA32) = {:.0f} mm²".format(As * 1e6))
    
    print("Test Treillis soudés")
    ST15C = ST("ST15C", True)
    print(ST15C)

    print("Paquet de barres")
    cnom = 50e-3
    phit = 12e-3
    bw = 350e-3
    dg = 35e-3
    
    phi = np.array([[32, 32, 32],
        [25, 25, 25],
        [25, 0, 25]]) * 1e-3
    print("Test 1 : 3 lits")
    print("yg = {:.3f} mm".format(CDG_acier3lits(phi, cnom, phit) * 1e3))
    print("yg = {:.3f} mm".format((3*78*32**2 + 3*106.5*25**2 + 2*131.5*25**2)/(3*32**2 + 5*25**2)))
    print("yg = {:.3f} mm".format(CDG_aciernlits(phi, dg, cnom, phit, bw, True) * 1e3))
    
    print("Test 2 : 4 lits")    
    phi = np.array([[32, 32, 32],
        [25, 25, 25],
        [25, 25, 25],
        [25, 25, 25]]) * 1e-3
    print("yg = {:.3f} mm".format(CDG_aciernlits(phi, dg, cnom, phit, bw, True) * 1e3))
    print("yg = {:.3f} mm".format((3*78*32**2 + 3*106.5*25**2 + 3*131.5*25**2 + 3*204.186*25**2)/(3*32**2 + 9*25**2)))

    print("Test 3 : ygj fourni")  
    ygj = np.array([[78, 78, 78],
       [106.5, 106.5, 106.5],
       [131.5, 131.5, 131.5],
       [204.186, 204.186, 204.186]]) * 1e-3
    print("yg = {:.3f} mm".format(CDG_aciernlits(phi, dg, cnom, phit, bw, True, ygj) * 1e3))
    print("Test phin")
    print("phi_n = {:.3f} mm".format(phin(phi)))
    print("Test enrobage")
    print("Test cmin_dur")
    ref, classe = "X0", 3
    cmintest = cmindurBA(ref, classe, True)
    phi = np.array([[32, 32, 32],
        [25, 25, 25],
        [25, 0, 25]]) * 1e-3
    print("Exposition : {0:s} S{1:d} -> cmindur = {2:.0f} mm".format(ref, classe, cmintest * 1e3))
    print("                     -> cminb = {0:.0f} mm".format(phin(phi) * 1e3))
    print(" Enrobage nominal        cnom = {0:.0f} mm".format(cnomBA(phi, ref, classe, dg) * 1e3))
    print("Test multiclasses")
    cmindurBA2("XC3 XD3", 3, True)
    print("Tant d'attrition")
    cminXM("XM2", True)
    print("Modulations de la classe structurale") #en bé majeur, le ton est donné)
    corr_classe_enrob("XC1", 1, True)
    corr_classe_duree100("XC1", 4, True)
    corr_classe_duree25("XC1", 5, True)
    corr_classe_resist("XC1", 5, 35., True)
    corr_classe_resist("XC1", 5, 70., True)
    print("Modulations tous critères")
    corr_classe_modulation(ref = "XD1", duree = 100., fck = 40., enrcompact = True, aff = True)
    dg = 40e-3
    cnom1 = cnomBA(phi, "XD1", 4, dg, True, "XM2")
    print("Exemple complet")
    refs = "XD1 XC3 XA1 XF1pf"
    fckmin, refMin = fckmindur(refs, True)
    [refCorr, cmin] = cmindurBA2(refs, 4, True)
    classe = corr_classe_modulation(ref = refCorr, duree = 100., fck = 40., enrcompact = True, aff = True)
    cnom = cnomBA(phi, refCorr, classe, dg, True, "XM2")
    ##### provisoire
#    print("Test bonne/mauvaise adhérence")
#    phiL = 5e-3
#    h = 125e-3
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, h/2., yHA(h/2., phiL, h)))
#    h = 255e-3
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, h / 2., yHA(h /2., phiL, h)))
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, 250e-3, yHA(250e-3, phiL, h)))
#    h = 300e-3
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, h / 2., yHA(h /2., phiL, h)))
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, 260e-3, yHA(260e-3, phiL, h)))
#    h = 700e-3
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, h / 2., yHA(h /2., phiL, h)))
#    print("h = {:.3f} yg = {:.3f} -> {:s}".format(h, 450e-3, yHA(450e-3, phiL, h)))
