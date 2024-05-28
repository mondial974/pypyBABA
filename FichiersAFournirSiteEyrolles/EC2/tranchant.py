#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: tranchant.py
"""
Module pour calculer le cisaillement dans les éléments en béton armé
"""
__version__ = '0.1'
import EC2.constantes as CST
import EC2.materiaux as MAT
#from math import pi
from math import pi, atan, sin, cos, tan

############################
### CISAILLEMENT TABLE Nervure
###########################

def FcdTe(ycu, beff, hf, bw, h, fck):
    """ effort de compression dans une section en té sans prise en compte des
    aciers comprimés
    entrée : ycu, beff, hf, h, [m], fck [MPa], sortie : [MN]"""
    if (ycu < hf / 0.8): #axe neutre dans la table
        return beff * 0.8 * ycu * MAT.fcd(fck)
    else:
        return ((beff - bw) * hf + bw * 0.8 * ycu ) * MAT.fcd(fck)

#### TRANCHANT
def alphacw(fck, sigmacp = 0):
    """ prise en compte de la membrure comprimée
    entrée : fck, sigmacp [MPa]
    sortie : []
    """
    fcd1 = MAT.fcd(fck)
    if (sigmacp < 0):
        raise ValueError("Attention Sigmacp > 0")
    elif (sigmacp < 0.25 * fcd1):
        return 1. + sigmacp / fcd1
    elif (sigmacp < 0.5 * fcd1):
        return 1.25
    elif (sigmacp < fcd1):
        2.5 * (1. - sigmacp / fcd1)
    else:
        raise ValueError("Attention Sigmacp < fcd")

def VRdcV(bw, d, Asl, typeBA, fck, aff = False, sigmacp = 0):
    """ effort tranchant résistant de calcul
        vmin annexe nationale
        typeBA : dalleredist -> dalle BA avecredistrib
               : dallepoutre -> poutre et dalle
               : voile
        entrée : bw, d [m], typeBA [], fck, sigmacp [MPa] 
        sortie : [MN]
    """
    CRdc = 0.18 / CST.GAMMAC
    k = min(1. + (200. / d * 1e-3)**.5, 2.)
    rhol = Asl / bw / d
    k1 = 0.15
    VRdc1 = (CRdc * k * (100. * rhol * fck)**(1. / 3.) + k1 * sigmacp) * bw *d
    if (typeBA == "dalleredist"):
        vmin1 = 0.23 * fck **0.5
    elif (typeBA == "dallepoutre"):
        vmin1 = 0.035 * k**1.5 * fck**0.5
    elif (typeBA == "voile"):
        vmin1 = 0.23 * fck**0.5
    else:
        raise ValueError("dalleredist, dallepoutre, voile seuls mots cles autorises")
    VRdc2 = (vmin1 + k1 * sigmacp)* bw * d 
    VRdc3 = max(VRdc1, VRdc2)
    if (aff):
        print(" CRdc = {:.3f} -- k = {:.3f} -- rhol = {:.3f} %"
              .format(CRdc, k, rhol * 1e2))
        print(" vmin = {:.3f} MPa".format(vmin1))
        print("VRdc = max ({:.3f}, {:.3f}) = {:.3f} MN"
              .format(VRdc1, VRdc2, VRdc3))
    return VRdc3

def VRdmaxV(bw, d, fck, aff = False, sigmacp = 0., theta = pi / 4., alpha = pi / 2.):
    """ effort tranchant résistant maximal
        entrée : bw, d [m], fck, sigmacp [MPa], theta, alpha [rad]
        sortie : [MN]
    """
    thetalim = atan(1. / 2.5)
    if (theta > pi / 4.) or (theta < thetalim):
        raise ValueError("1 < cotan Theta < 2.5")
    alphacw1 = alphacw(fck, sigmacp)
    z = .9 * d
    nu1 = 0.6 * (1. - fck / 250.)
    fcd1 = MAT.fcd(fck)
    VRdmax1 = alphacw1 * bw * z * nu1 * fcd1 * sin(theta)**2. * \
            (cos(theta) / sin(theta) + cos(alpha) / sin(alpha))
    if (aff):
        print(" z = {:.3f} m, nu1 = {:.3f}, fcd = {:.3f} MPa".format(z, nu1, fcd1))
        print("VRdmax = {:.3f} MN".format(VRdmax1))
    return VRdmax1

def slmax(d, aff = False, alpha = pi / 2.):
    """ espacement longitudinal maximal
    entrée : d [m], alpha [rad]
    sortie : [m]
    """
    slmax1 = 0.75 * d * (1. + cos(alpha) / sin(alpha))
    if (aff):
        print("slmax = {:.0f} mm".format(slmax1 * 1e3))
    return slmax1

def stmax(d, aff = False):
    """ espacement transversal maximal
    entrée : d [m], alpha [rad]
    sortie : [m]
    """
    stmax1 = min(0.75 * d, 0.6)
    if (aff):
        print("stmax = {:.0f} mm".format(stmax1 * 1e3))
    return stmax1

def Aswsmin(bw, fck, fyk, aff = True, alpha = pi / 2.):
    """ densité de ferraillage minimal d'effort tranchant 
    entrée : bw [m], fck, fyk [MPa], alpha [rad]
    sortie : [m²/m], soit des m
    """
    Aswmin1 = 0.08 * fck**0.5 / fyk * bw * sin(alpha)
    if (aff):
        print("Asw/sw)min > 1 / {0:.0f} cm²/cm = {1:.2f} cm²/m soit 2HA8 tous les {0:.0f} cm"
             .format(0.01 / Aswmin1, Aswmin1 * 1e4))
    return Aswmin1

def Aswsmax(bw, d, fck, fyk, aff = True, sigmacp = 0., theta = pi / 4., alpha = pi / 2.):
    """ densité de ferraillage maximal d'effort tranchant
    entrée : bw,d  [m], fck, fyk, sigmacp [MPa], alpha [rad]
    sortie : [m²/m], soit des m
    """
    alphacw1 = alphacw(fck, sigmacp)
    z = 0.9 *d
    nu1 = 0.6 * (1. - fck / 250.)
    fcd1, fywd1 = MAT.fcd(fck), MAT.fyd(fyk)
    Aswsmax1 = alphacw1 * bw * nu1 * fcd1 / fywd1 / (1. / tan(theta)**2. + 1.) / sin(alpha)
    if (aff):
        print(" alphacw = {:.3f}".format(alphacw1))
        print(" z = {:.3f} m, nu1 = {:.3f}, fcd = {:.3f} MPa".format(z, nu1, fcd1))
        print("Asw/sw)max < 1 / {0:.0f} cm²/cm = {1:.2f} cm²/m soit 2HA8 tous les {0:.0f} cm"
             .format(0.01 / Aswsmax1, Aswsmax1 * 1e4))
    return Aswsmax1

def AswsV(VEdu, d, fck, fyk, aff = True, theta = pi / 4., alpha = pi / 2.):
    """ densité de ferraillage d'effort tranchant
    entrée : VEdu  [MN] d [m], fck, fyk [MPa], alpha [rad]
    sortie : [m²/m], soit des m
    """
    fywd1 = MAT.fyd(fyk)
    z = 0.9 * d
    Asws1 = VEdu / (z * fywd1 * (1. / tan(theta) + 1. / tan(alpha)) * sin(alpha))
    if (aff):
        print("Asw/sw > 1 / {0:.0f} cm²/cm = {1:.2f} cm²/m soit 2HA8 tous les {0:.0f} cm"
              .format(0.01 / Asws1, Asws1 * 1e4))
    return Asws1

#### POINCONEMENT
def vRdcP(bw, d, Aslx, Asly, typeBA, fck, aff = False, sigmacp = 0):
    """ contrainte de cisaillement résistante de calcul pour le poinçonnement d'une dalle
        vmin annexe nationale
        typeBA : dalleredist -> dalle BA avecredistrib
               : dallepoutre -> poutre et dalle
               : voile
        entrée : bw, d [m], Aslx, Asly [m²], typeBA [], fck,sigmacp [MPa] 
        sortie : [MN]    """
    CRdc = 0.18 / CST.GAMMAC
    k = min(1. + (200. / d * 1e-3)**.5, 2.)
    rhox = Aslx / bw / d
    rhoy = Asly / bw / d
    rhol = min((rhox * rhoy)**0.5, 0.02)
    k1 = 0.1
    vRdc1 = CRdc * k * (100. * rhol * fck)**(1. / 3.) + k1 * sigmacp
    if (typeBA == "dalleredist"):
        vmin1 = 0.23 * fck **0.5
    elif (typeBA == "dallepoutre"):
        vmin1 = 0.035 * k**1.5 * fck**0.5
    elif (typeBA == "voile"):
        vmin1 = 0.23 * fck**0.5
    else:
        raise ValueError("dalleredist, dallepoutre, voile seuls mots cles autorises")
    vRdc2 = vmin1 + k1 * sigmacp
    vRdc3 = max(vRdc1, vRdc2)
    if (aff):
        print(" CRdc = {:.3f} -- k = {:.3f} -- rhol = {:.3f} %"
              .format(CRdc, k, rhol * 1e2))
        print(" vmin = {:.3f} MPa".format(vmin1))
        print("vRdc = max ({:.3f}, {:.3f}) = {:.3f} MPa"
              .format(vRdc1, vRdc2, vRdc3))
    return vRdc3

def vRdmaxP(fck, aff = False):
    """ contrainte de cisaillement résistante maximale au poinconnement
        entrée : fck [MPa], theta, alpha [rad]
        sortie : [MN]    """
    nu1 = 0.6 * (1. - fck / 250.)
    fcd1 = MAT.fcd(fck)
    vRdmax1 = 0.4 * nu1 * fcd1 
    if (aff):
        print(" nu1 = {:.3f}, fcd = {:.3f} MPa".format(nu1, fcd1))
        print("vRdmax = {:.3f} MPa".format(vRdmax1))
    return vRdmax1

def AswsuP(vEdu, bw, d, Aslx, Asly, typeBA, fck, fyk, aff = False, sigmacp = 0, alpha = pi / 2.):
    """ densité de ferraillage de poinconnement
    entrée : vEdu [MPa], bw, d, u1 [m], Aslx, Asly [m²], fck, fyk, sigmacp [MPa], alpha [rad], aff []
    sortie : [m²/m²], soit des m
    """
    vRdc1 = vRdcP(bw, d, Aslx, Asly, typeBA, fck, aff, sigmacp)
    fywdef1 = min(250. + .25e3 * d, MAT.fyd(fyk))
    Aswsr1 = (vEdu - 0.75 * vRdc1)  / (1.5 * sin(alpha) * fywdef1)
    if (Aswsr1 < 0):
        print(" Attention Aswsr négatif")
    if (aff):
        print(" fywd,eff = {:.2f} MPa".format(fywdef1))
        print("Asw/sr/u >  = {:.2f} cm²/m²".format(Aswsr1 * 1e4))
    return Aswsr1

def AswminuP(fck, fyk, aff = False, alpha = pi / 2.):
    """ section minimale [9.4.3(2)]
    entrée : st, sr [m], fck, fyk, [MPa], alpha [rad], aff []
    sortie : [m²/m²]
    """
    Aswmin1 = 0.08 * fck**0.5 / fyk / (1.5 * sin(alpha + cos(alpha)))
    if (aff):
        print("Section minimale Aswmin / sr / st > {:.1f} cm²/m²".format(Aswmin1 * 1e4))
    return Aswmin1

def DispoPoinc(d):
    """Affichage des dispositions constructives sur la répartition des cadres
    en poinçonnement
    entrée : d [m], aff []
    sortie : []"""
    print("Limitations géométriques [9.4.3]")
    print(" nombre de cours minimum 2")
    print(" x > 0.3 d = {:.1f} mm".format(0.3 * d * 1e3)) 
    print(" x < 0.5 d = {:.1f} mm".format(0.5 * d * 1e3))
    print(" st < 0.75 d = {:.1f} mm".format(0.75 * d * 1e3))
    print(" st < k d = 1.5 d  = {:.1f} mm".format(1.5 * d * 1e3))
    
### TORSION
def TRdmax(Ak, tefi, fck, aff = False, theta = pi / 4., sigmacp = 0.):
    """ effort de torsion maximal
    entrée : Ak [m²], tefi [m] fck, sigmacp [MPa] theta [rad] aff []
    sortie : [MN.m]
    """
    nu1 = 0.6 * (1. - fck / 250.)
    alphacw1 = alphacw(fck, sigmacp)
    TRdmax1 = 2. * alphacw1 * nu1 * MAT.fcd(fck) * Ak * tefi * sin(theta) * cos(theta)
    if (aff):
        print(" nu = {:.3f} alphacw = {:.3f}".format(nu1, alphacw1))
        print("TRdmax = {:.3f} MN.m".format(TRdmax1))
    return TRdmax1

def AkukRectPlein(tef, bw, h):
    """ aire balayée pour une section rectangulaire pleine, périmètre moyen 
    du feuillet
    entrée : tef, bw, h, [m]
    sortie : [m²], m"""
    return [(bw - tef) * (h - tef), 2 * (bw + h - 2 * tef)]

def TRdc(Ak, tefi, fck, aff = False):
    """ effort de torsion résistant
    entrée : Ak [m²], tefi [m] fck [MPa] aff []
    sortie : [MN.m]
    """
    TRdc1 = 2. * Ak * tefi * MAT.fctd(fck)
    if (aff):
        print("TRdc = {:.3f} MN.m".format(TRdc1))
    return TRdc1

def AswsT(TEdu, Ak, fyk, aff = False, theta = pi / 4.):
    """ densité de ferraillage de torsion
    entrée : TEdu [MN.m], Ak [m²], fyk [MPa], theta [rad], aff []
    sortie : [m²/m], soit des m
    """
    AswsT1 = TEdu / (2. * Ak * MAT.fyd(fyk)) * tan(theta)
    if (aff):
        print("Asw/sw > 1 / {0:.0f} cm²/cm = {1:.2f} cm²/m soit 2HA8 tous les {0:.0f} cm"
              .format(0.01 / AswsT1, AswsT1 * 1e4))
    return AswsT1

def AslT(TEdu, Ak, uk, fyk, aff = False, theta = pi / 4.):
    """ section d'acier longitudinaux à la torsion
    entrée : TEdu [MN.m], Ak [m²], uk [m], fyk [MPa], theta [rad], aff []
    sortie : [m²/m], soit des m
    """
    AslT1 = TEdu * uk / (2. * Ak * MAT.fyd(fyk) * tan(theta))
    if (aff):
        print("Asl > {0:.0f} mm²".format(AslT1 * 1e6))
    return AslT1

def uLminRectPlein(bw, h):
    """ périmètre et distance mini de la section rectangulaire pleine
    entrée : bw, h [m]
    sortie : [m, m]"""
    return [2. * (bw + h), min(bw, h)]

def slmaxT(d, u, lmin, aff = False, alpha = pi / 2.):
    """ espacement longitudinal maximal pour la torsion
    entrée : d, u, lmin [m], alpha [rad]
    sortie : [m]
    """
    slmax1 = min(slmax(d, aff, alpha), u / 8., lmin)
    if (aff):
        print("slmax = {:.0f} mm".format(slmax1 * 1e3))
    return slmax1

def AswsminT(tef, fck, fyk, aff = True, alpha = pi / 2.):
    """ densité de ferraillage minimal à la torsion
    entrée : tef [m], fck, fyk [MPa], alpha [rad]
    sortie : [m²/m], soit des m
    """
    Aswmin1 = Aswsmin(tef, fck, fyk, aff, alpha)
    return Aswmin1

### CISAILLEMENT TABLE/NERVURE
def vRdchf(fck, typeSurf, aff = False):
    """ contrainte en dessous de laquelle aucune armature de cisaillement
    table nervure n'est necessaire
    entrée fck [MPa], typeSurf [lisse, rugueuse]
    sortie [MPa]"""
    if (typeSurf in CST.KTABLENERV.keys()): #classes initiales
        k = CST.KTABLENERV[typeSurf] 
    else:
        s = ""
        for cle in CST.KTABLENERV.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour K = {0:s}".format(typeSurf))
    vRdchf1 = k * MAT.fctd(fck)
    if (aff):
        print(" k = {:.2f} pour surface {:s}".format(k, typeSurf))
        print("vRd,c = {:3f} MPa".format(vRdchf1))
    return vRdchf1
        


def vRdmaxhf(fck, thetaf, aff = False, comp = True, ):
    """ contrainte de cisaillement résistant maximal pour la membrure
        entrée : bw, d [m], fck, sigmacp [MPa], thetaf [rad]
        sortie : [MPa]
    """
    thetalimp, thetalimm = atan(1. / 2.), atan(1. / 1.25)
    if (comp): #compression
        if (thetaf > pi / 4.) or (thetaf < thetalimp):
            raise ValueError("en compression 1 < cotan Theta < 2")        
    else:
        if (thetaf > pi / 4.) or (thetaf < thetalimm):
            raise ValueError("en traction 1 < cotan Theta < 1.25")        
    nu1 = 0.6 * (1. - fck / 250.)
    fcd1 = MAT.fcd(fck)
    vRdmax1 = nu1 * fcd1 * sin(thetaf) * cos(thetaf)
    if (aff):
        print("vRdmax = {:.3f} MPa".format(vRdmax1))
    return vRdmax1
    
def Asfsf(vEdu, hf, fck, fyk, thetaf, aff = True):
    """ densité de ferraillage d'effort tranchant table nervure
    entrée : d, hf [m] vedu, fck, fyk [MPa], thetaf [rad]
    sortie : [m²/m], soit des m
    """
    fyd1 = MAT.fyd(fyk)
    Asfsf1 = vEdu * hf * tan(thetaf) / fyd1
    if (aff):
        print("Asw/sw > 1 / {0:.0f} cm²/cm = {1:.2f} cm²/m soit 2HA8 tous les {0:.0f} cm"
              .format(0.01 / Asfsf1, Asfsf1 * 1e4))
    return Asfsf1

def AsfsfFlex(vEdu, hf, fck, fyk, Ap, Am, thetaf, aff = True):
    """ densité de ferraillage d'effort tranchant table nervure
    entrée : d, hf [m] vedu, fck, fyk [MPa], Ap, Am [m2/m] thetaf [rad]
    sortie : [m²/m], soit des m
    """
    Asfsf1 = Asfsf(vEdu, hf, fck, fyk, thetaf, False)
    Asfsf1 = max(Asfsf1, 0.5 * Asfsf1 + (Ap + Am))
    if (aff):
        print("Asw/sw > 1 / {0:.0f} cm²/cm = {1:.2f} cm²/m soit 2HA8 tous les {0:.0f} cm"
              .format(0.01 / Asfsf1, Asfsf1 * 1e4))
    return Asfsf1

### SURFACE DE REPRISE
def vRdi(c, mu, fck, fyk, As, Ai, sigmaN, aff = False, alpha = pi /2.):
    """ contrainte de cisaillement sur la surface de reprise
    entrée : c, mu [], fck, sigmaN [MPa] As, Ai [m²], aff [], alpha [rad]
    sortié : [MPa]"""
    vRdi1 = mu * sigmaN
    fctd1, fcd1 = MAT.fctd(fck), MAT.fcd(fck)
    if (sigmaN > 0):
        vRdi1 = vRdi1 + c * fctd1
    rho = As / Ai
    vRdi1 = vRdi1 + rho * MAT.fyd(fyk) * (mu * sin(alpha) + cos(alpha))
    nu1 = 0.6 * (1. - fck / 250.)
    vRdi2 = 0.5 * nu1 * fcd1
    vRdi3 = min(vRdi1, vRdi2)
    if (aff):
        print(" c = {:.3f} mu = {:.3f} rho = {:.3f}".format(c, mu, rho))
        print(" fctd = {:.3f} MPa fcd = {:.3f} MPa".format(fctd1, fcd1))
        print(" nu1 ={:.3f}".format(nu1))
        print("vRdi = min(vRdi, 0.5 nu fcd) =min({:.3f}, {:.3f}) = {:.3f} MPa"
              .format(vRdi1, vRdi2, vRdi3))
    return vRdi3

def etatsurf(typeSurf):
    """ etat de surface
    entree : treslisse, lisse, rugueux, indentation 
    sortie : [c, µ]
        """
    if (typeSurf == 'treslisse'):
        return [0.25, 0.5]
    if (typeSurf == 'lisse'):
        return [0.35, 0.6]
    if (typeSurf == 'rugueux'):
        return [0.45, 0.7]
    if (typeSurf == 'indentation'):
        return [0.50, 0.9]
    raise ValueError("Mots clés autorisés : treslisse, lisse, rugueux, indentation ")
       
if __name__ == "__main__":
    import EC2.dispositionsconstructives as DC
    print("Cisaillement d'une dalle")
    bw, d = 1., 0.150
    fck = 25.
    Asl = DC.ST("ST25")[0]
    typeBA = "dallepoutre"    
    VRdcV(bw, d, Asl, typeBA, fck,  True)
    print("Cisaillement d'une poutre")
    bw, d = 0.3, 0.482
    fck = 25.
    Asl = DC.HA(3, 25)
    typeBA = "dallepoutre"    
    VRdcV(bw, d, Asl, typeBA, fck,  True)
    VRdmaxV(bw, d, fck, True)
    slmax(d, True)
    stmax(d, True)
    fyk = 500.
    Aswsmin(bw, fck, fyk, True)
    Aswsmax(bw, d, fck, fyk, True)
    VEdu = 0.195
    rep = AswsV(VEdu, d, fck, fyk, True)
    Asw = DC.HA(3, 8)
    print("so < {:.1f} mm".format(Asw / rep * 1e3))
    print("Poinçonnement d'une dalle")
    bw, d = 1., 95e-3
    Aslx, Asly = DC.HA(5, 12), DC.HA(5, 8)
    fck = 25.
    vRdcP1 = vRdcP(bw, d, Aslx, Asly, "dallepoutre",  fck)
    vRdmaxP(fck, True)
    u1 = 1.674
    vEdu = 0.707
    AswsP(vEdu, bw, d, u1, Aslx, Asly, "dallepoutre", fck, fyk, True)
    sr, st =50e-3, 120e-3
    AswminP(st, sr, fck, fyk, True)
    DispoPoinc(d)
    print("Torsion d'une poutre")
    bw, h, d = 0.36, 0.750, 0.675 #m
    fck = 25. #MPa
    tefi = 90e-3 #m
    TEdu = 0.06526
    Ak, uk = AkukRectPlein(tefi, bw, h)
    TRdmax(Ak, tefi, fck, True)
    TRdc(Ak, tefi, fck, True)
    AswsT(TEdu, Ak, fyk, True)
    AslT(TEdu, Ak, uk, fyk, True)
    u, lmin = uLminRectPlein(bw, h)
    slmaxT(d, u, lmin, True)
    AswsminT(tefi, fck, fyk, True)
    print("Cisaillement table/nervure")
    thetaf = atan(1. / 2.)
    hf = 0.15
    fck = 25.
    vEdu = 0.881 #MPa
    vRdmaxhf(fck, thetaf, True)
    r = Asfsf(vEdu, hf, fck, fyk, thetaf, True)
    Ap, Am = DC.ST("ST15C")[0], DC.ST("ST15C")[0]
    AsfsfFlex(vEdu, hf, fck, fyk, Ap, Am, thetaf, True)
    print("Cisaillement surface de reprise")
    c, mu = etatsurf("rugueux")
    fck = 25.
    As = DC.HA(10, 32)
    bw, li = 0.2, 2.5
    Ai = bw * li
    sigmaN = 0.4 #MPa
    vRdi(c, mu, fck, fyk, As, Ai, sigmaN, True)