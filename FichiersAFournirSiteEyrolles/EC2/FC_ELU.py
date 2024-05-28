#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: FC_ELU.py
"""
Module pour calculer les aciers dans un cadre de flexion composée 
"""
__version__ = '0.1'
import EC2.constantes as CST
import EC2.materiaux as MAT

from scipy.optimize import fsolve
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, tan, pi


def VecteurAbaquesNM(v, vp, d, dp, fck, epsilonuk, bNonSymetrique = False, nbpts = [100, 100, 100]):
    """
    calcul des paramètres eps0 et ki de la droite de déformation (3 pivots)
    entrée : v, vp, d, dp, [m], fck [MPa], epsilonuk [],
    sortie : eps0 [], lambda [m-1]
    """   
    epsud = MAT.epsilonud(epsilonuk)
    epscu2 = - MAT.epsiloncu2(fck)
    epsc2= - MAT.epsilonc2(fck)    
    h = v + vp
    #partie supérieure
    nbpts_z1, nbpts_z2, nbpts_z3 = nbpts
    #zone 1, pivot A, traction simple, traction excentrée, flexion simple
    epsP = np.linspace(epsud, epscu2, nbpts_z1)
    ki = [ (epsP1 - epsud) / d for epsP1 in epsP]
    eps0 = [ (epsud * v - epsP1 * (v - d)) / d for epsP1 in epsP]
    #eps0 = [ epsud - kii * (v - d) for kii in ki]
    #zone 2, pivot B, flexion simple, flexion composée
    epsM2 = (epsud * v + epscu2 * (v - d)) / d + (epscu2 + epsud) / d * vp
    epsM = np.linspace(epsM2, 0, nbpts_z2)
#    epsM = np.linspace(epsM2, -epscu2, nbpts_z2)
#    epsM = np.concatenate((epsM, np.linspace(-epscu2, 0, nbpts_z2)), axis = 0)
    ki = np.append(ki, [(epscu2 - epsM21) / h for epsM21 in epsM])
    eps0 = np.append(eps0, [(epscu2 * vp + epsM21 * v) / h for epsM21 in epsM])
    #zone 3, pivot C, flexion composée, compression simple
    dc = h * (epscu2 - epsc2)/epscu2
    epsP = np.linspace(epscu2, epsc2, nbpts_z3)
    ki = np.append( ki, [(epsP1 - epsc2) / dc for epsP1 in epsP])
    eps0 = np.append( eps0, [(epsc2 * v - epsP1 * (v - dc)) / dc for epsP1 in epsP])
    if (bNonSymetrique):
        ## partie inférieure si besoin
        #zone 3
        dcp = h * epsc2 / epscu2
        epsP = np.linspace(epsc2, 0, nbpts_z3)
        ki = np.append( ki, [(epsP1 - epsc2) / dcp for epsP1 in epsP])
        eps0 = np.append( eps0, [(epsc2 * v - epsP1*(v - dcp)) / dcp for epsP1 in epsP])
        #zone 2
        epsP2 = (epsud * vp + epscu2 * (v - dp)) / (h - dp) + (epsud - epscu2) / (h - dp) * v
        epsP = np.linspace(0, epsP2, nbpts_z2)
        ki = np.append(ki, [(epsP21 - epscu2) / h for epsP21 in epsP])
        eps0 = np.append(eps0, [(epscu2 * v + epsP21 * vp) / h for epsP21 in epsP])
        #zone 1
        epsM = np.linspace(epscu2, epsud, nbpts_z1)
        ki = np.append(ki, [ (epsud - epsM1) / (h - dp) for epsM1 in epsM])
        eps0 = np.append( eps0, [ (epsud * vp + epsM1 * (v - dp)) / (h - dp) for epsM1 in epsM])
    return [eps0, ki]


def PointsParticuliersAbaquesNM(v, vp, d, dp, fck, epsilonuk, bNonSymetrique = False):
    """
    calcul des paramètres paticuliers aux changements de zone pour les 3 pivots
    entrée : v, vp, d, dp, [m], fck [MPa], epsilonuk [],
    sortie : eps0 [], lambda [m-1]
    """   
    epsud = MAT.epsilonud(epsilonuk)
    epscu2 = - MAT.epsiloncu2(fck)
    epsc2= - MAT.epsilonc2(fck)
    h = v + vp
    #partie supérieure
    #zone 1, pivot A, pivot B
    epsP = [epsud, epscu2]
    ki = [ (epsP1 - epsud) / d for epsP1 in epsP]
    eps0 = [ (epsud * v - epsP1 * (v - d)) / d for epsP1 in epsP]
    #zone 2, pivot B, pivot C
    epsM2 = (epsud * v + epscu2 * (v - d)) / d + (epscu2 + epsud) / d * vp
    epsM = [epsM2, 0]
    ki = np.append(ki, [(epscu2 - epsM21) / h for epsM21 in epsM])
    eps0 = np.append(eps0, [(epscu2 * vp + epsM21 * v) / h for epsM21 in epsM])
    #zone 3, pivot C
    dc = h * (epscu2 - epsc2) / epscu2
    epsP = [epscu2, epsc2]
    ki = np.append( ki, [(epsP1 - epsc2) / dc for epsP1 in epsP])
    eps0 = np.append( eps0, [(epsc2 * v - epsP1 * (v - dc)) / dc for epsP1 in epsP])
    ## partie supérieure si besoin   
    if (bNonSymetrique):
        ## partie supérieure si besoin
        #zone 1
        epsM = [epsud, epscu2]
        ki = np.append(ki, [ (epsud - epsM1) / (h - dp) for epsM1 in epsM])
        eps0 = np.append( eps0, [ (epsud * vp + epsM1 * (v - dp)) / (h - dp) for epsM1 in epsM])
         #zone 2 
        epsP2 = (epsud * vp + epscu2 * (v - dp)) / (h - dp) + (epsud - epscu2)/(h - dp) * v
        epsP = [epsP2, 0]
        ki = np.append(ki, [(epsP21 - epscu2) / h for epsP21 in epsP])
        eps0 = np.append(eps0, [(epscu2 * v + epsP21 * vp) / h for epsP21 in epsP])
        #zone 3
        dcp = h * epsc2/epscu2
        epsP = [0, epsc2]
        ki = np.append( ki, [(epsP1 - epsc2) / dcp for epsP1 in epsP])
        eps0 = np.append( eps0, [(epsc2 * v - epsP1 * (v - dcp)) / dcp for epsP1 in epsP])
    return [eps0, ki]


def b(y, geom):
    """ largeur de la section à traiter en fonction de geom
    entrée : y [m], geom
    sortie : [m]"""
    if ("RECT" in geom):
        v, vp, bw = geom["RECT"]
        return bw
    if ("TE" in geom):
        v, vp, hf, bw, beff = geom["TE"]
        if (y > v - hf):
            return beff
        else:
            return bw
    if ("CIRC" in geom):
        v, vp, R = geom["CIRC"]
        return 2. * (R * R  - y * y)**.5
    raise ValueError("Cle non reconnue dans b")

def Nc(eps0, ki, v, vp, geom, fck):
    """	Effort normal résistant béton pour une section rectangulaire
    entrée : eps0 [], ki [m-1], v, vp, geom [m], fck [MPa]
    sortie : [MN]
    """
    def integrand(y, eps0, ki, fck, geom):
        return b(y, geom) * MAT.sigmac2(eps0 + ki * y, fck)
    return quad(integrand, -vp, v, args = (eps0, ki, fck, geom))[0]

def Mc(eps0, ki, v, vp, geom, fck):
    """	Moment fléchissant résistant béton pour une section rectangulaire
    entrée : eps0 [], ki [m-1], v, vp [m], fck [MPa]
    sortie : [MN]    """
    def integrand(y, eps0, ki, fck, geom):
        return - b(y, geom) * MAT.sigmac2( eps0 + ki * y, fck) * y
    return quad(integrand, -vp, v, args = (eps0, ki, fck, geom))[0]

def NM_C_S(eps0, ki, v, vp, geom, fck, fyk, Aciers):
    """efforts résistants béton et acier
    entrée : eps0 [], lambda [m-1], v, vp, d, dp, [m], fck, fyk [MPa], Aciers [m², m],
    sortie : Nrc [MN], Mrc [MN.m] NRs [MN] MRs [MN.m]"""
    Nrc = Nc(eps0, ki, v, vp, geom, fck)
    Mrc = Mc(eps0, ki, v, vp, geom, fck)
    Nrs = sum([ MAT.sigmas1(eps0 + ki * ysi, fyk) * Asi for Asi, ysi in Aciers])
    Mrs = sum([ - ysi * MAT.sigmas1(eps0 + ki * ysi, fyk) * Asi for Asi, ysi in Aciers])
    return [Nrc, Mrc, Nrs, Mrs]

def TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll = [[], []], bNonSymetrique = False, nbpts = [100, 100, 100]):
    """ tracé de l'abaque d'interaction pour la section 
    entrée : v, vp, geom [m], fck, fyk [MPa], epsilonuk [], soll = [[MN], [MN.m]]
    sortie : NMr, NMrpt [MN, MM.m, MN, MN.m]
    geom est un dictionnaire pour
    geom = {"RECT": [v, vp, bw]}
         = {"TE": [v, vp, hf, bw, beff]}
         = {"CIRC": [v, vp, D]}
    """
    d, dp = v - min(Aciers[:, 0]), vp - max(Aciers[:, 0])
    h = v + vp
    [eps0, ki] = VecteurAbaquesNM(v, vp, d, dp, fck, epsilonuk, bNonSymetrique, nbpts)
    [eps0p, kip] = PointsParticuliersAbaquesNM(v, vp, d, dp, fck, epsilonuk, bNonSymetrique)
    NMr = np.array([NM_C_S(eps0C, kiC, v, vp, geom, fck, fyk, Aciers) for eps0C, kiC in zip(eps0, ki)])
    NMrPt = np.array([NM_C_S(eps0C, kiC, v, vp, geom, fck, fyk, Aciers) for eps0C, kiC in zip(eps0p, kip)])
    
    plt.figure()
    plt.plot(NMr[:, 0], NMr[:, 1], 'k')
    plt.plot(NMrPt[:, 0], NMrPt[:, 1], 'k*')
    
    plt.plot(NMr[:, 0] + NMr[:, 2], NMr[:, 1] + NMr[:, 3], 'k-')
    plt.plot(NMrPt[:, 0] + NMrPt[:, 2], NMrPt[:, 1] + NMrPt[:, 3], 'k*')
    
    #placment des sollicitations
    NEdu, MEdu = soll
    plt.plot(NEdu, MEdu, 'k*')
    plt.grid('on')
    plt.xlabel(r'$N_{Rd}$ [MN]')
    plt.ylabel(r'$M_{Rd}$ [MN.m]')
    if ("RECT" in geom):
        v, vp, bw = geom["RECT"]
        plt.title(u"Abaque d'interaction d'une section rectangulaire - {:.0f}x{:.0f} mm²". \
              format(bw * 1e3, h * 1e3))
        plt.savefig('./AbaqueInteractionRect-{:.0f}x{:.0f}.pdf'. \
                format(bw * 1e3, h * 1e3))
    if ("TE" in geom):
        v, vp, hf, bw, beff = geom["TE"]
        plt.title(u"Abaque d'interaction d'une section en té - {:.0f}x{:.0f} mm²". \
              format(bw * 1e3, h * 1e3))
        plt.savefig('./AbaqueInteractionTe-{:.0f}x{:.0f}.pdf'. \
                format(bw * 1e3, h * 1e3))
    if ("CIRC" in geom):
        v, vp, R = geom["CIRC"]
        plt.title(u"Abaque d'interaction d'une section circulaire - {:.0f} mm". \
              format(R * 1e3))
        plt.savefig('./AbaqueInteractionCirc-{:.0f}.pdf'. \
                format(R * 1e3))
    return [NMr, NMrPt]

def TraceAbaqueNormalisee(v, vp, geom, fck, fyk, epsilonuk, Aciers, 
                          bNonSymetrique = False, 
                          soll = [[], []], nbpts= [100, 100, 100]):
    """ tracé de l'abaque d'interaction normalisée pour la section 
    entree : v, vp, geom [m], fck, fyk [MPa], epsilonuk [], Aciers [m², m]
    sortie : n1, n2 []
    geom est un dictionnaire pour
    geom = {"RECT": [v, vp, bw]}
         = {"TE": [v, vp, hf, bw, beff]}
         = {"CIRC": [v, vp, D]}
    """
    fcd1, fyd1 = MAT.fcd(fck), MAT.fyd(fyk)
    d, dp = v - min(Aciers[:, 0]), vp - max(Aciers[:, 0])
    h = v + vp
    [eps0, ki] = VecteurAbaquesNM(v, vp, d, dp, fck, epsilonuk, bNonSymetrique, nbpts)
    [eps0p, kip] = PointsParticuliersAbaquesNM(v, vp, d, dp, fck, epsilonuk, bNonSymetrique)
    NMr = np.array([NM_C_S(eps0C, kiC, v, vp, geom, fck, fyk, Aciers) for eps0C, kiC in zip(eps0, ki)])
    NMrPt = np.array([NM_C_S(eps0C, kiC, v, vp, geom, fck, fyk, Aciers) for eps0C, kiC in zip(eps0p, kip)])
    if ("RECT" in geom) or ("CIRC" in geom):
        Astot = sum(Aciers[:,0])
        if ("RECT" in geom):
            v, vp, bw = geom["RECT"]
        if ("CIRC" in geom):
            v, vp, R = geom["CIRC"]
            bw = pi * R / 2. #de manière à avoir bw h = aire du cercle h = D
        [nurc, murc, nurs, murs] = [ NMr[:,0] / bw / h / fcd1, \
                                     NMr[:,1] / bw / h / h / fcd1, \
                                     NMr[:,2] / Astot / fyd1,\
                                     NMr[:,3] / Astot / h / fyd1]
        [nurcPt, murcPt, nursPt, mursPt] = [ NMrPt[:,0] / bw / h / fcd1, \
                                             NMrPt[:,1] / bw / h / h / fcd1, \
                                             NMrPt[:,2] / Astot / fyd1, \
                                             NMrPt[:,3] / h / Astot / fyd1]
        n1, n2 = [nurc, murc, nurs, murs], [nurcPt, murcPt, nursPt, mursPt] 
        #courbes normalisées
        plt.figure()
        omega1 = Astot * fyd1 / (bw * h * fcd1)
        nbCourbes = 20.
        nu1 = nurc + omega1 * nurs
        mu1 = murc + omega1 * murs
        plt.plot(nu1, mu1, 'k--')
        for i in range(int(nbCourbes) + 1):
            omega = i / nbCourbes
            #courbes
            nu1 = nurc + omega * nurs
            mu1 = murc + omega * murs
            plt.plot(nu1, mu1, 'k-')
            #points particuliers
            nu1Pt = nurcPt + omega * nursPt
            mu1Pt = murcPt + omega * mursPt
            plt.plot(nu1Pt, mu1Pt, 'k.')
            
        nb  =  int(nbCourbes + 1)
        x  =  np.linspace(-1,  -1.68,  nb +1)
        y  =  0  +  (x  +  1) / (-1.68  +  1) * 0.145
        for i,  xi,  yi in zip(range(nb),  x,  y):
            if (i % 4  ==  0):
                plt.text(xi,  yi,  str(100  /  (nb - 1) * i)  +  " %",  size = 6,  bbox = dict(boxstyle = "square", fc = (1, 1, 1)))
        
        dec  =  - 0.2
        plt.text(xi  +  dec,  (xi  +  dec  +  1) / (-1.68  +  1) * 0.145,  '$\omega  =  \dfrac{\sum A_s}{b_w h}\ \dfrac{f_{yd}}{f_{cd}}$',  size = 6,  bbox = dict(boxstyle = "square", fc = (1, 1, 1)))
        
        plt.grid(True)
        if ("RECT" in geom):
            NEdu, MEdu = soll
            plt.plot(np.array(NEdu) / bw / h / fcd1, 
                     np.array(MEdu)  / bw / h**2. / fcd1, 'k*')
            plt.xlabel(r'$\frac{N}{b_w h f_{cd}}$ []')
            plt.ylabel(r'$\dfrac{M}{b_w h^2 f_{cd}}$ []')
            plt.title(u"Courbe d'interaction section rectangulaire")
            #axes().set_aspect('equal')
            plt.savefig("./InteractionRectangulaire-{:.0f}x{:.0f}mm².pdf".format(bw * 1e3, h * 1e3))       
        if ("CIRC" in geom):
            NEdu, MEdu = np.array(soll)
            plt.plot(np.array(NEdu) / R**2. / fcd1, 
                     np.array(MEdu) / R**3. / fcd1, 'k*')
            plt.xlabel(r'$\frac{N}{\pi R^2 f_{cd}}$ []')
            plt.ylabel(r'$\dfrac{M}{\pi R^3 / 2 f_{cd}}$ []')
            plt.title(u"Courbe d'interaction section circulaire")
            #axes().set_aspect('equal')
            plt.savefig("./InteractionCirculaire-{:.0f}x{:.0f}mm².pdf".format(R * 1e3, R * 1e3))            
        return [n1, n2]
    else:
        print("Section non reconnue ... clés acceptées RECT CIRC")
        return [[], []]
    
if __name__ == "__main__":
    plt.close('all')
#    print("Section rectangulaire")
#    bw = 0.200 #m largeur de la section
#    h = 0.700 #m hauteur de la section
#    v, vp = h / 2., h / 2. #position du centre de gravité 
#    geom = {"RECT": [v, vp, bw]}
#    fck = 30.0 #MPa,  résistance du béton en compression
#    d = 0.630 #m position du centre de gravité des aciers tendus
#    As = 2113e-6 #m² section aciers tendus
#    dp = 0.07 #m position du centre de gravité des aciers comprimés
#    Asp = 2113e-6 #m² section aciers comprimés
#    fyk = 500.0  #MPa résistance de l'acier
#    epsilonuk = 5e-2
#    Aciers = np.array([[As, (h / 2. - d)],
#              [Asp, h / 2. - dp]])
#    NEdu = np.array([-2, -3.871]) #MN
#    MEdu = np.array([0.3, 0.2     ]) #0.05558 #0.043 #MN.m
#    soll = [NEdu, MEdu] 
#    [eps0, ki] = VecteurAbaquesNM(v, vp, d, dp, fck, epsilonuk)
#    [eps0p, kip] = PointsParticuliersAbaquesNM(v, vp, d, dp, fck, epsilonuk)
#    #vérification
#    plt.figure()
#    plt.grid('on')
#    X, Y = np.zeros(2), np.zeros(2)
#    Y = [v, -vp]
#    for i, (eps0i, kii) in enumerate(zip(eps0, ki)):
#        X = np.array([eps0i + kii * v, eps0i - kii * vp])
#        if (i % 5 == 0) : plt.plot(X * 1e2, Y, 'k-')
#    plt.xlabel(r'$\epsilon$ [%]')
#    plt.ylabel(r'y [m]')
#    plt.savefig('./3pivots.pdf')
#    [NMr, NMrpt] = TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll, 
#                                True, [100, 500, 100]) #dble True
#    [NMrNorm, NMrNormpt] = TraceAbaqueNormalisee(v, vp, geom, fck, fyk, epsilonuk, 
#                                Aciers,  False, [[],[]], [100, 500, 100])
    ## VOILE
#    print("Voile")
#    bw = .25 #m largeur de la section
#    h = 2.500 #m hauteur de la section
#    v, vp = h / 2., h / 2. #position du centre de gravité 
#    geom = {"RECT": [v, vp, bw]}
#    fck = 30.0 #MPa,  résistance du béton en compression
#    fyk = 500.0  #MPa résistance de l'acier
#    epsilonuk = 5e-2
#
#    NEdu = np.array([-2, -3.871]) #MN
#    MEdu = np.array([-1.15, 0.]) #0.05558 #0.043 #MN.m
#    soll = [NEdu, MEdu]
#
#    Aciers =np.array([[ 1608e-6, -1.186],
#                      [ 1608e-6, -1.111],
#                      [ 1608e-6, -1.036],
#                      [ 1608e-6, -0.961],
#                      [ 1608e-6, -0.886],
#                      [ 1608e-6, -0.811],
#                      [  157e-6, -0.651],
#                      [  157e-6, -0.491],
#                      [  157e-6, -0.331],
#                      [  157e-6, -0.171],
#                      [  157e-6, -0.0011],
#                      [  157e-6,  0.149],
#                      [  157e-6,  0.309],
#                      [  157e-6,  0.469],
#                      [  157e-6,  0.629],
#                      [  157e-6,  0.789],
#                      [ 1608e-6,  0.864],
#                      [ 1608e-6,  0.939],
#                      [ 1608e-6,  1.014],
#                      [ 1608e-6,  1.089],
#                      [ 1608e-6,  1.164],
#                      [ 1608e-6,  1.239]])
#    [NMr, NMrpt] = TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll, True, [100, 500, 100])
#    plt.show()
    ## TE
#    print("Section en té")
#    bw = 0.300 #m largeur de la section
#    beff = 2.00 #m, largeur efficace de la section
#    h = 0.900 #m hauteur de la section
#    hf = 0.20 #m eépaisseur de la dalle
#    v, vp = h / 2., h / 2. #position du centre de gravité 
#    geom = {"TE": [v, vp, hf, bw, beff]}
#    fck = 30.0 #MPa,  résistance du béton en compression
#    d = 0.85 #m position du centre de gravité des aciers tendus
#    As = 2113e-6 #m² section aciers tendus
#    dp = 0.05 #m position du centre de gravité des aciers comprimés
#    Asp = 1500e-6 #m² section aciers comprimés
#    fyk = 500.0  #MPa résistance de l'acier
#    epsilonuk = 5e-2
#
#    Aciers = np.array([[As, (h / 2. - d)],
#              [Asp, h / 2. - dp]])
#    NEdu = np.array([-2, -3.871]) #MN
#    MEdu = np.array([0.3, 0.2     ]) #0.05558 #0.043 #MN.m
#    soll = [NEdu, MEdu]
#    
#    [NMr, NMrpt] = TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll, True)
#    [NMrNorm, NMrNormpt] = TraceAbaqueNormalisee(v, vp, geom, fck, fyk, epsilonuk, Aciers)
    ## CIRCULAIRE
    print("Section circulaire")
    R = 0.300 #m rayon de la section
    v, vp = R, R #position du centre de gravité 
    geom = {"CIRC": [v, vp, R]}
    fck = 30.0 #MPa,  résistance du béton en compression
    fyk = 500.0  #MPa résistance de l'acier
    epsilonuk = 5e-2

    Asi = 201e-6 #HA 16
    Rsi = 0.9 * R
    nsi = 10
    ##démarrage au sommet, assez favorable
    Aciers = np.array([[Asi, Rsi * cos( 2. * pi * float(i) / nsi) ] for i in range(nsi)])
    
    NEdu = np.array([-2, -3.871]) #MN
    MEdu = np.array([0.3, 0.2     ]) #0.05558 #0.043 #MN.m
    soll = [NEdu, MEdu]
    
    [NMr, NMrpt] = TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll, True, [100, 500, 100])
    [NMrNorm, NMrNormpt] = TraceAbaqueNormalisee(v, vp, geom, fck, fyk, epsilonuk, Aciers)
#    print("Section rectangulaire")
#    import dispositionsconstructives as DC
#    bw, h = 250e-3, 1000e-3
#    fck, fyk = 20., 500.
#    phi = 2.
#    As = DC.HA(6, 25)
#    Asp = As #DC.HA(3, 12) + DC.HA(3, 8)
#    dp, d = 67e-3, 917e-3
#    v, vp = h / 2., h / 2. #position du centre de gravité 
#    geom = {"RECT": [v, vp, bw]}
#    epsilonuk = 5e-2
#    Aciers = np.array([[As, (h / 2. - d)],
#              [Asp, h / 2. - dp]])
#    NEdu = np.array([-2, -3.871]) #MN
#    MEdu = np.array([0.3, 0.2     ]) #0.05558 #0.043 #MN.m
#    soll = [NEdu, MEdu] 
#    [eps0, ki] = VecteurAbaquesNM(v, vp, d, dp, fck, epsilonuk)
#    [eps0p, kip] = PointsParticuliersAbaquesNM(v, vp, d, dp, fck, epsilonuk)
#    [NMr, NMrpt] = TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll, True, [2, 20, 2])
#    [NMrNorm, NMrNormpt] = TraceAbaqueNormalisee(v, vp, geom, fck, fyk, epsilonuk, Aciers, True)
