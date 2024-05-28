#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: instabilites.py
"""
Module pour calculer les instabilités
"""
__version__ = '0.1'
import EC2.materiaux as MAT
import EC2.constantes as CST

from scipy.optimize import fsolve
from scipy.integrate import quad
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from math import pi, atan, cos, sin

def AireGeom(geom):
    """ renvoie l'aire d'une section classique
    entrée : geom [m]
    sortie : [m²]"""
    if ("RECT" in geom):
        v, vp, bw = geom["RECT"]
        return bw * (v + vp)
    if ("TE" in geom):
        v, vp, hf, bw, beff = geom["TE"]
        return bw * (v + vp - hf) + beff * hf
    if ("CIRC" in geom):
        v, vp, R = geom["CIRC"]
        return pi * R * R
    raise ValueError("Cle non reconnue dans geom via AireGeom")

def InertieGeom(geom):
    """ renvoie l'inertie d'une section classique
    entrée : geom [m]
    sortie : [m²]"""
    if ("RECT" in geom):
        v, vp, bw = geom["RECT"]
        return bw * (v + vp)**3. / 12.
    if ("TE" in geom):
        v, vp, hf, bw, beff = geom["TE"]
        Ac = AireGeom(geom)
        return bw * (v + vp)**3. / 3. + (beff - bw) * hf**3. - Ac * v**2.
    if ("CIRC" in geom):
        v, vp, R = geom["CIRC"]
        return pi * R ** 4. / 4.
    raise ValueError("Cle non reconnue dans geom via IntertieGeom")

def RayonGirationGeom(geom):
    """ renvoie le rayon de giration d'une section classique
    entrée : geom [m]
    sortie : [m]"""
    return (InertieGeom(geom) / AireGeom(geom))**.5    

def lambdalim(geom, fck, NEdu, A = .7, B = 1.1, C = .7, aff = False):
    """ Elancement limite pour éléments isolés [5.8.3.1]
    entrée : geom [m], fck [MPa], NEdu [MN], fyk [MPa]
    sortie : []"""
    Ac = AireGeom(geom)
    n = abs(NEdu) / ( Ac * MAT.fcd(fck))
    Llim1 = 20. * A * B * C / n**.5
    if (aff):
        print("Elancement limite : Llim = {:.3f}".format(Llim1))
        print(" Par défaut, A=.7, B=1.1, C=.7...")
        print(" A = {:.3f} B = {:.3f} C = {:.3f}".format(A, B, C))
        print(" Ac = {:.3f} m² NEdu = {:.3f} MN n = {:.3f}".
              format(Ac, abs(NEdu), n))
    return Llim1

def thetai(lo, m = 1, aff = False):
    """imperfection angulaire initiale [5.2(5)]
    entrée : lo [m], m []
    sortie : [rad]"""
    theta0 = 1. / 200.
    alphah = min( max(2. / lo**.5, 2. / 3.), 1.)
    alpham = (.5 * (1. + 1. / m))**.5
    thetai1 = theta0 * alphah * alpham
    if (aff):
        print(" Imperfection angulaire initale thetai = {:.3f} rad".
              format(thetai1))
        print(" theta0 = {:.4f} alpha_h = {:.4f} alpham = {:.3f} m = {:.0f}".
              format(theta0, alphah, alpham, m))
    return thetai1

def e0i(lo, m = 1, aff = False):
    """excentricité liée aux imperfections [5.2.(6)] plus AN
    entrée : lo [m], m []
    sortie : [m]"""
    e01i = max(thetai(lo, m, aff) * lo / 2., 2e-2)
    if (aff):
        print(" Excentricité initiale e0 = {:.3f} m".format(e01i))
    return e01i

def RigiditeNominale(lambda1, Lo, geom, phieff, fck, Aciers, fyk, NEdu, MEdu0, 
                         beta = 1, aff = False):
    """ Moment basé sur une estimation de la courbure nominale
    entrée : lambda1 [] Lo [m] geom [m], phieff [] fck [MPa] Aciers [m²,m], 
             fyk [MPa] NEdu [MN] MEdu0 [MN.m] beta = 1 [] -> [5.8.7.3],
    sortie : [MN.m]"""
    
    Ac = AireGeom(geom)
    As = sum([Asi for Asi, ysi in Aciers])
    rho = Ac / As
    if (rho > 0.0002):
        Ks = 1.
        k1 = (fck / 20.)**.5
        n = abs(NEdu) / Ac / MAT.fcd(fck)
        k2 = min(n * lambda1 / 170., .2)
        Kc = k1 * k2 / (1. + phieff)
        Ecd = MAT.Ecm(fck) / CST.GAMMACE
        Ic = InertieGeom(geom)
        Es1 = CST.ES
        Is = sum([Asi * ysi**2. for Asi, ysi in Aciers]) #néglige inertie propre
        EI = Kc * Ecd * Ic + Ks * Es1 * Is
        NB = EI * pi**2. / Lo**2.
        MEduRN = MEdu0 * (1. + beta / (NB / abs(NEdu) - 1.))
        if (aff):
            print("Méthode de la rigidité nominale : MEdu = {:.3f} MN.m".
                  format(MEduRN))    
            print(" Ks = {:.0f} Es1 = {:.0f} MPa Is = {:.0f} mm4".
                  format(Ks, Es1, Is * 1e12))
            print(" Kc = {:.3f} Ecd = {:.0f} MPa Ic = {:.0f} mm4".
                  format(Kc, Ecd, Ic * 1e12))
            print("  -> k1 = {:.3f} k2 = {:.3f}".format(k1, k2))
            print(" NB = {:.3f} MN\n".format(NB))
            return MEduRN
    else:
        raise ValueError("rho < 0.0002 : RigiditeNominale")
        
        
def CourbureNominale(lambda1, Lo, geom, phieff, fck, Aciers, fyk, NEdu, MEdu0, 
                     c = 8, aff = False):
    """ estimation du moment par la méthode de la courbure nominale [5.8.8]
    entrée : lambda1 [] Lo [m] geom [m], phieff [] fck [MPa] Aciers [m²,m], 
             fyk [MPa] NEdu [MN] MEdu0 [MN.m] c = 8 [] -> [5.8.8.2(4)],
    sortie : [MN.m]"""
    beta = .35 + fck / 200. - lambda1 / 150.
    Kphi = max(1. + beta * phieff, 1.)
    Ac = AireGeom(geom)
    fcd1 = MAT.fcd(fck)
    n = abs(NEdu) / (Ac * fcd1)
    nbal = .4
    As = sum([Asi for Asi, ysi in Aciers])
    fyd1 = MAT.fyd(fyk)
    omega = As * fyd1 / (Ac * fcd1)
    nu = 1. + omega
    Kr = min((nu - n) / (nu - nbal), 1.)
    epsyd = fyd1 / CST.ES
    Is = sum([Asi * ysi**2.0 for Asi, ysi in Aciers])
    irays = (Is / As)**.5
    for key, value in geom.iteritems(): #parcours uniquement premiere valeur
        h = value[0] + value[1]
    d = h / 2. + irays
    r01 = epsyd / (.45 * d)
    r1 = Kr * Kphi * r01
    e2 = r1 * Lo**2. / c
    M2 = abs(NEdu) * e2
    MEduCN = MEdu0 + M2
    if (aff):
        print("Méthode de la courbure nominale : MEdu = {:.3f} MN.m".
                  format(MEduCN))    
        print(" Kphi = {:.3f} beta = {:.3f}".format(Kphi, beta))
        print(" Kr = {:.3f} nu = {:.3f} omega = {:.3f}".
              format(Kr, nu, omega))
        print(" nbal = {:.3f} n = {:.3f}".format(nbal, n))
        print(" 1/r0 = {:.4f} m-1 epsyd = {:.5f} is = {:.3f} m".
              format(r01, epsyd, irays))
        print("  d = {:.3f} m".format(d))
        print(" r1 = {:.4f} m-1".format(r1))
        print(" e2 = {:.3f} m M2 = {:.3f} MN.m\n".format(e2, M2))
    return MEduCN
    
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

def Nc(eps0, ki, v, vp, geom, phi, fck):
    """	Effort normal résistant béton pour une section rectangulaire
    entrée : eps0 [], ki [m-1], v, vp, geom [m], fck [MPa]
    sortie : [MN]
    """
    def integrand(y, eps0, ki, geom, phi, fck):
        return b(y, geom) * MAT.sigmac1(eps0 + ki * y, phi, fck)
    return quad(integrand, -vp, v, args = (eps0, ki, geom, phi, fck))[0]

def Mc(eps0, ki, v, vp, geom, phi, fck):
    """	Moment fléchissant résistant béton pour une section rectangulaire
    entrée : eps0 [], ki [m-1], v, vp [m], fck [MPa]
    sortie : [MN]    """
    def integrand(y, eps0, ki, geom, phi, fck):
        return - b(y, geom) * MAT.sigmac1( eps0 + ki * y, phi, fck) * y
    return quad(integrand, -vp, v, args = (eps0, ki, geom, phi, fck))[0]

def EqN(eps0, ki, v, vp, geom, phi, fck, Aciers, fyk, NEdu):
    """ equation d'équilibre de l'effort normal
    entrée : eps0 [], ki [m-1], vp, vp , geom [m], phi [], fck [MPa]
             Aciers [m², m], fyk [MPa], NEdu [MN]
    sortie : [MN]"""        
    return NEdu - (Nc(eps0, ki, v, vp, geom, phi, fck) \
                + sum([ MAT.sigmas1(eps0 + ki * ysi, fyk) * Asi for Asi, ysi in Aciers]))


def MethodeGenerale(e0, Lo, v, vp, geom, phi, fck, Aciers, fyk, NEdu, kimax = 80e-3, kimin = 0., nbpts = 50, aff = False):
    """ méthode général permettant le calcul du moment au second ordre
    entrée : 
    sortie : [MN.m] et graphiques"""
    ki = np.linspace(0, kimax, nbpts)
    eps0 = np.array([fsolve(EqN, 0.000, 
             args = (kii, v, vp, geom, phi, fck, Aciers, fyk, NEdu))[0] for
            kii in ki])
    MRds = np.array([sum([ - ysi * MAT.sigmas1(eps0i + kii * ysi, fyk) * Asi 
                          for Asi, ysi in Aciers]) 
                          for eps0i, kii in zip(eps0, ki)])
    MRdc = np.array([Mc(eps0i, kii, v, vp, geom, phi, fck) 
                     for eps0i, kii in zip(eps0, ki)])
    e1 = (MRdc + MRds) / NEdu #excentricité interne	
    e2 = e0 + (Lo / pi)**2.0 * ki #excentricité externe
    alf = atan((Lo / pi)**2.0)
    xe1rot = cos(alf) * ki + sin(alf) * e1
    ye1rot =  - sin(alf) * ki + cos(alf) * e1
    xe2rot = cos(alf) * ki + sin(alf) * e2
    ye2rot =  - sin(alf) * ki + cos(alf) * e2
    imax = np.nanargmax(xe1rot)
    print("Indice maxi  =  {0:d}  val  =  {1:.3f} ".format(imax, ye1rot[imax]))
    print("Excentricité associée e1 =  {0:.3f}".format(e1[imax]))
    print("Moment associée MRdu = {:.3f} MN.m".format(e1[imax] * abs(NEdu)))

#    NRds = np.array([sum([ MAT.sigmas1(eps0i + kii * ysi, fyk) * Asi 
#                          for Asi, ysi in Aciers]) 
#                          for eps0i, kii in zip(eps0, ki)])
#    NRdc = np.array([Nc(eps0i, kii, v, vp, geom, phi, fck)
#                     for eps0i, kii in zip(eps0, ki)])
#    NRdu = NRds + NRdc    
    plt.figure()
    plt.grid(True)
    plt.xlabel(r'$\chi$ [10$^3$m$^{- 1}$]')
    plt.ylabel(r'e [m]')
    plt.title(u'Loi excentricité courbure')  
    plt.plot(ki * 1e3, e1, 'k+')
    plt.plot(ki * 1e3, e1, 'k')
    plt.plot(ki * 1e3, e2, 'k-')
    #plt.savefig("./images/ExcentriciteCourbure1.pdf")
    f = interpolate.interp1d(ki, e1)
    def eqF(x, e0, Lo, f):
        return f(x) - (e0 + (Lo / pi)**2.0 * x)
    [ki1N, info, ier, mesg] = fsolve(eqF, 0., args = (e0, Lo, f), full_output = True)
    ki1N = ki1N[0]
    if (mesg != 'The solution converged.'):
        print("Pas de solution")
        raise ValueError(mesg)
    else:
        plt.plot(ki1N * 1e3, f(ki1N), 'g*')
        if (aff):
            print("Excentricité totale e = {:.3f} m".format(f(ki1N)))
            if (ki1N < ki[imax]):
                print("Equilibre stable")
            else:
                print("Equilibre instable")
            print("Moment sollicitant intégrant les effets du second ordre : MEdu = {:.3f} MN.m".
                  format(f(ki1N) * abs(NEdu)))
    plt.savefig("./images/ExcentriciteCourbure1b.pdf")
    return abs(NEdu) * f(ki1N)
    
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    import dispositionsconstructives as DC
    import FC_ELU as FC
    plt.close('all')
    print("Flambement de mon poto")
    bw = 0.35 #m largeur de la section
    h = 0.35 #m hauteur de la section
    fck = 30.0 #[MPa], résistance du béton
    phi = 2 #[], coefficient de fluage du béton
    v, vp = h / 2., h / 2.
    geom = {"RECT": [v, vp, bw]}
    dp = 0.05
    d = h - dp #m position du centre de gravité des aciers tendus
    As = DC.HA(2, 20) #m² section aciers tendus
    #m position du centre de gravité des aciers comprimés
    Asp = As #m² section aciers comprimés
    fyk = 500. #{MPa], résistance de l'acier
    Aciers = np.array([[As, (h / 2. - d)],
                       [Asp, h / 2. - dp]])
    Ng = - 0.3 #MN
    Nq = - 0.2 #MN
    Mg = 0.02 #MN.m
    Mq = 0.02
    psi2 = 0.3
    NEdu = 1.35 * Ng + 1.5 * Nq
    MEdqp = Mg + psi2 * Mq
    MEdu0 = 1.35 * Mg + 1.5 * Mq
    phieff = phi * MEdqp / MEdu0
    
    Lo = 5. #m, longueur de flambement
    e0 = e0i(Lo, aff = True) #m, excentricité initiale
    ei = e0 + MEdu0 / abs(NEdu)
    MEdui = abs(NEdu) * ei
    
    #élancement limite
    Llim = lambdalim(geom, fck, NEdu, aff = True)
    A1 = 1. / (1. + .2 * phieff)
    omega = sum([Asi for Asi, ysi in Aciers]) * MAT.fyd(fyk) / \
            (AireGeom(geom) * MAT.fcd(fck))
    B1 = (1. + 2. * omega)**.5
    rm = 1.
    C1 = 1.7 - rm
    Llim = lambdalim(geom, fck, NEdu, aff = True, A = A1, B = B1, C = C1)
    ipot = RayonGirationGeom(geom)
    Lpot = Lo / ipot
    print("Elancement réel du poteau : Lpot = {:.3f}\n".format(Lpot))        
    MEduCN = CourbureNominale(Lpot, Lo, geom, phieff, fck, 
                              Aciers, fyk, NEdu, MEdui, 
                              c = pi**2., aff = True)

    MEduRN = RigiditeNominale(Lpot, Lo, geom, phieff, fck, 
                              Aciers, fyk, NEdu, MEdui, 
                              beta = pi**2. / 8., aff = True)
    MEduMG = MethodeGenerale(ei, Lo, v, vp, geom, phi, fck, Aciers, fyk, NEdu, 
                    kimax = 40e-3, kimin = 0., nbpts = 50, aff = True)
    print('NEdu = {:.3f} MN'.format(NEdu))
    epsilonuk = 5e-2
    soll2 = [[NEdu, NEdu, NEdu], [MEdui + MEduCN,MEdui + MEduRN, MEdui + MEduMG]]
    FC.TraceAbaques(v, vp, geom, fck, fyk, epsilonuk, Aciers, soll2,  False, [100, 500, 100])
    FC.TraceAbaqueNormalisee(v, vp, geom, fck, fyk, epsilonuk, Aciers, False, soll2, [100, 500, 100])
    #loi de comportement béton [3.1.7]
    ##test du tracé des courbes de comportement
    eps = np.linspace( - MAT.epsiloncu1(fck) - 0.01, 0.001, 1000)
    sigc = [MAT.sigmac1(epsi, phi, fck) for epsi in eps]
    sigc1 = [MAT.sigmac1(epsi, 0., fck) for epsi in eps]
    plt.figure()
    plt.plot(eps * 1e2, sigc, 'k-', label=r'$\varphi=2$')
    plt.plot(eps * 1e2, sigc1, 'k--', label =r'$\varphi=0$' )
    plt.xlabel(r'$\epsilon_c$ [%]')
    plt.ylabel(r'$\sigma_c$ [MPa]')
    plt.grid('on')
    plt.legend()
    plt.title(u"Lois de comportement du béton [3.1.5] pour " 
              + r"$f_{ck}$ = " + u"{:.0f} MPa et ".format(fck)
              + r"$\varphi$ = " +  u"{:.0f} et 0". format(phi))
    plt.savefig('./images/LC1.pdf')   
#
#    ###méthode générale exemple 1
#    ki = 10e-3 #m - 1
#    eps0 = fsolve(EqN, - 0.000, 
#                  args = (ki, v, vp, geom, phi, fck, Aciers, fyk, NEdu))[0]
#    print("ki =  {0:.3f} m-1 eps0 = {1:.6f}".format(ki, eps0))
#    NRds = sum([ MAT.sigmas1(eps0 + ki * ysi, fyk) * Asi for Asi, ysi in Aciers])
#    MRds = sum([ - ysi * MAT.sigmas1(eps0 + ki * ysi, fyk) * Asi for Asi, ysi in Aciers])
#    NRdc = Nc(eps0, ki, v, vp, geom, phi, fck)
#    MRdc = Mc(eps0, ki, v, vp, geom, phi, fck)
#    print(" NEdu = {:.3f} MN\n NRdu = {:.3f} MN, Nrdc = {:.3f} MN NRds = {:.3f} MN".
#          format(NEdu, NRdc + NRds, NRdc, NRds)) 
#    print(" MRdu = {:.3f} MN.m MRdc = {:.3f} MN.m MRds = {:.3f} MN.m".
#          format(MRdc + MRds, MRdc, MRds))
#    
#    ##méthode générale résolution complète
#    nbpts = 50
#    kimax = 80e-3 
#    #JALON 1 ou le mystère du grand retour
#    
#    ki = np.linspace(0, kimax, nbpts)
#    eps0 = np.array([fsolve(EqN, 0.000, 
#             args = (kii, v, vp, geom, phi, fck, Aciers, fyk, NEdu))[0] for
#            kii in ki])
#    MRds = np.array([sum([ - ysi * MAT.sigmas1(eps0i + kii * ysi, fyk) * Asi 
#                          for Asi, ysi in Aciers]) 
#                          for eps0i, kii in zip(eps0, ki)])
#    MRdc = np.array([Mc(eps0i, kii, v, vp, geom, phi, fck) 
#                     for eps0i, kii in zip(eps0, ki)])
#    e1 = (MRdc + MRds) / NEdu #excentricité interne	
#    e2 = e0 + (Lo / pi)**2.0 * ki #excentricité externe
#    NRds = np.array([sum([ MAT.sigmas1(eps0i + kii * ysi, fyk) * Asi 
#                          for Asi, ysi in Aciers]) 
#                          for eps0i, kii in zip(eps0, ki)])
#    NRdc = np.array([Nc(eps0i, kii, v, vp, geom, phi, fck)
#                     for eps0i, kii in zip(eps0, ki)])
#    NRdu = NRds + NRdc
#    
#    p1 = plt.figure()
#    plt.grid(True)
#    plt.xlabel(r'$\chi$ [m$^{ - 1}$]')
#    plt.ylabel(r'e [m]')
#    plt.title(u'Loi excentricité courbure')  
#    plt.plot(ki, e1, 'r+')
#    plt.plot(ki, e1, 'b')
#    plt.plot(ki, e2, 'm')
#    plt.savefig("./images/ExcentriciteCourbure1.pdf")
#
#    f = interpolate.interp1d(ki, e1)
#    def eqF(x, e0, Lo, f):
#        return f(x) - (e0 + (Lo / pi)**2.0 * x)
#    [ki1N, info, ier, mesg] = fsolve(eqF, 0., args = (e0, Lo, f), full_output = True)[0]
#    if (mesg != 'The solution converged.'):
#        print("Pas de solution")
#    else:
#        plt.plot(ki1N, f(ki1N), 'g*')
#        print("Moment sollicitanti intégrant les effets du second ordre : MEdu = {:.3f} MN.m".
#          format(f(ki1N) * NEdu))
#    plt.savefig("./images/ExcentriciteCourbure1b.pdf")
    
#    #JALON 2
#    alf = atan((Lo / pi)**2.0)
#    print("alpha  =  {0:.3f}".format(alf * 180.0 / pi))
#    x1rot = cos(alf) * ki + sin(alf) * e1
#    e1rot = - sin(alf) * ki + cos(alf) * e1
#    x2rot = cos(alf) * ki + sin(alf) * e2
#    e2rot = - sin(alf) * ki + cos(alf) * e2
#    #JALON 3 
#    #recherche du maximum
#    imax = np.nanargmax(e1rot)
#    print("indice maxi  =  {0:d}  val  =  {1:.3f} ".format(imax, e1rot[imax]))
#    print("val initiale  =  {0:.3f}".format(e1[imax]))
#
#    #interpolation
#    plt.plot([0, max(ki)], 
#              [e1[imax] - (Lo / pi)**2.0 * ki[imax], 
#               e1[imax] - (Lo / pi)**2.0 * ki[imax] + (Lo / pi)**2.0 * max(ki)],'r-')
#    plt.savefig("./images/ExcentriciteCourbure2.pdf")
#    plt.show()
#    
#    plt.figure()
#    plt.grid('on')
#    plt.plot(x1rot, e1rot, 'r+')
#    plt.plot(x1rot, e1rot, 'b')
#    plt.plot(x2rot, e2rot, 'm')
#    plt.savefig('./images/Erot.pdf')
#    g = interpolate.interp1d(x1rot, e1rot)
#    e2max = max(e2rot)
#    def eqF(x, e2max, g):
#        return f(x) - e2max
#    x1rotN = fsolve(eqF, 0., args = (e2max, g))[0]
#    plt.plot(x1rotN, g(x1rotN), 'r*')
