#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: FS_ELS.py
"""
Module pour calculer les aciers dans un contexte de flexion simple
"""
__version__ = '0.1'
import EC2.constantes as CST
import EC2.materiaux as MAT
from math import exp
import EC2.mathBA as MATBA
from scipy.optimize import fsolve

############################
### SECTION RECTANGULAIRE
###########################

def MRcFlex(bw, d, fck, sigstL, sigccL,  phiinf):
    """moment résistant béton
    entrée : bw,d, [m], fck,fyk, [MPa], wmax, [mm], phinf[], sortie : [MN.m]
    dimensionnement à la volée en 1000 wmax en flexion"""
    #sigstL = 1000*wmax
    #sigccL = 0.6*fck 
    alphae = CST.ES / MAT.Ecm(fck) * (1. + phiinf / 1.05) 
    alphaL = alphae * sigccL / (alphae * sigccL + sigstL)
    return alphaL / 2. * (1. - alphaL / 3) * bw * d**2 * sigccL


def AsqpFlex(MEdqp, bw, d, d1, fck, sigstL, sigccL, phiinf):
    """moment résistant béton
    entrée : bw,d,d1 [m], fck,fyk, [MPa], wmax, [mm], phinf[], sortie : [m²]			  
    dimensionnement à la volée en 1000 wmax"""
    #sigstL = 1000*wmax
    #sigccL = 0.6*fck
    alphae = CST.ES / MAT.Ecm(fck) * (1 + phiinf / 1.05)
    alphaL = alphae * sigccL / (alphae * sigccL + sigstL)
    MRcFlex1 = alphaL / 2. * (1. - alphaL / 3) * bw * d**2 * sigccL
    if (MEdqp <= MRcFlex1):#sans aciers comprimés
        mus = MEdqp / (bw * d**2 * sigstL / alphae)
        alpha1c = MATBA.solve3deg(1, -3, -6*mus, 6*mus)
        #zc1 = 15/16*(40*mus+1)/(54*mus+1)*d formule simplifiée
        zc1 = d* (1 - alpha1c / 3)
        return [MEdqp / (zc1 * sigstL), 0]
    else: #avec aciers comprimés
        yqp = alphaL * d
        sigsc1 = alphae * sigccL * (yqp-d1) / yqp
        A1qp = (MEdqp - MRcFlex1) / (d-d1) / sigsc1
        zcL = d * (1. - alphaL / 3)
        AspqpFlex = (MEdqp - MRcFlex1) / (d - d1) / sigsc1
        return [MRcFlex1 / zcL / sigstL + A1qp * sigsc1 / sigstL, AspqpFlex]

def zcFlex(MEdqp, bw, d, d1,  fck, sigstL, sigccL, phiinf ):
    """moment résistant béton
    entrée : bw,d,d1 [m], fck,fyk, [MPa], wmax, [mm], phinf[], sortie : [m²]
    dimensionnement à la volée en 1000 wmax"""
    alphae = CST.ES / MAT.Ecm(fck) * (1.0 + phiinf / 1.05)
    alphaL = alphae * sigccL / (alphae * sigccL + sigstL)
    MRcFlex1 = alphaL / 2. * (1. - alphaL / 3) * bw * d**2 * sigccL
    if (MEdqp <= MRcFlex1): #sans aciers comprimés
        mus = MEdqp / (bw * d**2 * sigstL / alphae)
        alpha1c = MATBA.solve3deg(1, -3, -6*mus, 6*mus)
        #zc1 = 15/16*(40*mus+1)/(54*mus+1)*d formule simplifiée
        return d * (1 - alpha1c / 3)
    else: #avec aciers comprimés
        return d * (1. - alphaL / 3)

def AsRectXSDF(MEdc, MEdqp, bw, d, d1,  fck, sigstL, sigccL, phiinf, aff = False):
    """section d'acier en conditions XS, XD, XF et 0.8 fyk, ELS seul
    entrée : bw,d,d1 [m], fck,fyk, [MPa], wmax, [mm], phinf[], sortie : [m²]			  
    dimensionnement en caractéristique"""
    alphae = CST.ES / MAT.Ecm(fck) * (1. + MEdqp / MEdc * phiinf / 1.05)
    alphaL = alphae * sigccL / (alphae * sigccL + sigstL)
    MRcFlex1 = alphaL / 2. * (1. - alphaL / 3) * bw * d**2 * sigccL
    if (MEdc <= MRcFlex1): #sans aciers comprimés
        mus = MEdc / (bw * d**2 * sigstL / alphae)
        alpha1c = MATBA.solve3deg(1, -3, - 6*mus, 6*mus)
        #zc1 = 15/16*(40*mus+1)/(54*mus+1)*d formule simplifiée
        zc1 = d * (1 - alpha1c / 3)
        As = MEdc / (zc1 * sigstL)
        if (aff):
            print("MEd,c = {0:.3f} MN.m MEdqp = {1:.3f} MN.m".format(MEdc, MEdqp))
            print("alphae = {0:.3f} alphaL = {1:.3f} MRc = {2:.2f} MN.m".format(alphae, alphaL, MRcFlex1))
            print("mus = {0:.3f} alpha1c = {1:.3f} zc = {2:.3f} m".format(mus, alpha1c, zc1))
            print("As >= {0:.1f} mm² As' >= {1:.2f} mm²".format(As * 1e6, 0))
        return [As, 0.0]
    else: #avec aciers comprimés
        yc = alphaL * d
        sigsc1 = alphae * sigccL * (yc - d1) / yc
        A1c = (MEdc - MRcFlex1) / (d - d1) / sigsc1
        zcL = d * (1. - alphaL / 3)
        As = MRcFlex1 / zcL / sigstL + A1c * sigsc1 / sigstL
        if (aff):
            print("MEd,c = {0:.3f} MN.m MEdqp = {1:.3f} MN.m".format(MEdc, MEdqp))
            print("alphae = {0:.3f} alphaL = {1:.3f} MRc = {2:.2f} MN.m".format(alphae, alphaL, MRcFlex1))
            print("yc = {0:.3f} m sigs' = {1:.3f} MPa zcL = {2:.3f} m".format(yc, sigsc1, zcL))
            print("As >= {0:.1f} mm² As' >= {1:.2f} mm²".format(As * 1e6, A1c * 1e6))
        return [As , A1c]


##############################################################################
### VERIFICATION CONTRAINTES SECTION RECTANGULAIRE
##############################################################################

def VerifContRect(MEd, As, Asp, bw, h, d, dp, fck, fyk, phi, k, aff = False):
    """ Vérification des contraintes à l'ELS section rectangulaire
    entree: MEd:[MN.m] As, Asp :[m²] bw,d,dp:[m] fck:[MPa] phi,k:[] 
    sortie: [m, m4, MPa]"""
    [Ach, v, vp, Ich, Mfiss1, Mfiss2] = MfissRect(As, Asp, bw, h, d, dp, phi, fck, aff)
    alphae = CST.ES / MAT.Ecm(fck) * (1. + phi / 1.05)
    if (MEd > 0): 
        Mfiss = Mfiss1
    else:
        Mfiss = Mfiss2
    if (abs(MEd) < Mfiss): #section non fissurée
        if (aff):
            print("Section non fissurée")
        K = MEd / Ich
        if (MEd > 0): 
            yser = v
        else:
            yser = vp
        Iser = Ich
    else: #section en calcul fissurée
        if (aff):
            print("Section fissurée")
        if (MEd > 0):
            a, b, c = bw / 2., alphae * (As + Asp), - alphae * (d * As + dp * Asp)
        else:
            a, b, c = bw / 2., alphae * (As + Asp), - alphae * ((h - d) * As + (h - dp) * Asp)
            
        def eq(y, a, b, c):
            return a * y**2.0 + b * y + c
        yser = fsolve(eq, 0, args = (a, b, c))[0]
        if (MEd > 0):
            Iser = bw * yser**3 / 3. + alphae * Asp * (yser - dp)**2  \
                    + alphae * As * (d - yser)**2
        else:
            Iser = bw * yser**3 / 3. + alphae * Asp * (yser - h + dp)**2  \
                    + alphae * As * (h - d - yser)**2            
        K = MEd / Iser
    sigc = K * yser
    if (MEd > 0):
        sigs = alphae * K * (d - yser)
        sigst = alphae * K * (yser - dp)
    else:
        sigs = alphae * K * (h - d - yser)
        sigst = alphae * K * (yser - h + dp)        
    if (aff):
        print("Vérification des contraintes section rectangulaire")
        print(" alphae = {:.3f}".format(alphae))
        print(" yser = {:3f} m Iser = {:.6f} m4".format(yser, Iser))
        print(" sigc = {:.2f} MPa < ? < {:.2f} MPa = {:.1f} fck".format(sigc, k * fck, k))
        if (sigc > k * fck): print(" ----- PB -------")
        print(" sigs = {:.2f} MPa < ? < {:.2f} MPa = 0.8 fyk".format(sigs, 0.8 * fyk))
        if (sigs > 0.8 * fyk): print(" ----- PB -------")
        print(" sigs' = {:.2f} MPa".format(sigst))
    return [alphae, yser, Iser, sigc, sigs, sigst]

def MfissRect(As, Asp, bw, h, d, dp, phi, fck, aff = False):
    """moment de fissuration 
    entrée: As, Asp :[m²] bw,h,d,dp:[m] phi:[] 
    sortie: [m², m, m, m4, MN.m, MN.m]"""
    alphae = CST.ES / MAT.Ecm(fck) * (1. + phi / 1.05)
    Ach = bw * h + alphae * (As + Asp)
    v = (bw * h**2.0 /2 + alphae * (As * d + Asp * dp)) / Ach
    vp = h - v
    Ich = bw * h**3 / 12. + bw * h * (h / 2 - v)**2.0 + \
          alphae * As * (d - v)**2. + alphae * Asp * (v - dp)**2. 
    fcteff1 = MAT.fctm(fck)
    Mfiss1 = fcteff1 * Ich / vp
    Mfiss2 = fcteff1 * Ich / v
    if (aff):
        print("Moment de fissuration sous M > 0 : Mfiss = {:.3f} MN.m".format(Mfiss1))
        print("Moment de fissuration sous M < 0 : Mfiss = {:.3f} MN.m".format(Mfiss2))
        print(" alphae = {:.3f}, fctm = {:.3f} MPa".format(alphae, fcteff1))
        print(" Ach = {:.3f} m², v = {:.3f} m, v' = {:.3f} m, Ich = {:.6f} m4".format(Ach, v, vp, Ich))
    return [Ach, v, vp, Ich, Mfiss1, Mfiss2]
    

def MRdqp(fck, Iqp, yqp, aff = False):
    """ moment résistant en quasi permanent
    entrée: k[], fck [MPa], Iqp [m4] yqp:[m], sortie:[MN.m]""" 
    MRdqp1 = 0.45 * fck * Iqp / yqp
    if (aff):
        print("Moment résistant (0.45fck) : MRdqp = {:.3f} MN.m".format(MRdqp1))
    return MRdqp1

def MRdc(fck, fyk, d, Ic, yc, alphae, aff = False):
    """ moment résistant en caractéristique
    entrée: k[], fck [MPa], Iqp [m4] yqp:[m], sortie:[MN.m]""" 
    MRdc1, MRdc2 = 0.6 * fck * Ic / yc, 0.8 * fyk * Ic / (d - yc) / alphae
    MRdc3 = min(MRdc1, MRdc2)
    if (aff):
        print("Moment résistant (0.6fck) : MRdc = {:.3f} MN.m".format(MRdc1))
        print("Moment résistant (0.8fyk) : MRdc = {:.3f} MN.m".format(MRdc2))
        print("Moment résistant          : MRdc = {:.3f} MN.m".format(MRdc3))
    return MRdc3

##############################################################################
### VERIFICATION CONTRAINTES SECTION EN TE
##############################################################################

def VerifContTe(MEd, As, Asp, beff, bw, hf, d, dp, fck, fyk, phi, k, aff = False):
    """ Vérification des contraintes à l'ELS section rectangulaire
    entree: MEd:[MN.m] As, Asp :[m²] bw,d,dp:[m] fck:[MPa] phi,k:[] sortie: [m, m4, MPa]"""
    [Ach, v, vp, Ich, Mfiss1, Mfiss2] = MfissTe(As, Asp, beff, bw, hf, h, d, dp, phi, fck, aff)
    alphae = CST.ES / MAT.Ecm(fck) * (1. + phi / 1.05)
    if (MEd > 0): 
        Mfiss = Mfiss1
    else:
        Mfiss = Mfiss2
    if (abs(MEd) < Mfiss): #section non fissurée
        if (aff):
            print("Section non fissurée")
        K = MEd / Ich
        yser = v
        Iser = Ich
    else: #section en calcul fissurée
        alphae = CST.ES / MAT.Ecm(fck) * (1. + phi / 1.05)
        a = bw / 2.
        b = (beff - bw) * hf + alphae * (As + Asp) 
        c = - ((beff - bw) * hf**2.0 / 2.0 + alphae * (d * As + dp * Asp))
        def eq(y, a, b, c):
            return a * y**2.0 + b * y + c
        if (eq(hf) > 0): #calcul en section rectangulaire pour bw = beff
            [alphae, yser, Iser, sigc, sigs, sigst] = VerifContRect(MEd, 
                As, Asp, beff, h, d, dp, fck, fyk, phi, k)   
        else: #calcul en section en té
            yser = fsolve(eq, 0, args = (a, b, c))[0]
            Iser = beff * yser**3 / 3. - (beff - bw) * (yser - hf)**3.0 / 3.0 \
             + alphae * Asp * (yser - dp)**2  \
             + alphae * As * (d - yser)**2
        K = MEd / Iser
    sigc = K * yser
    sigs = alphae * K * (d - yser)
    sigst = alphae * K * (yser - dp)
    if (aff):
        print("Vérification des contraintes section rectangulaire")
        print(" alphae = {:.3f}".format(alphae))
        print(" yser = {:3f} Iser = {:.6f} m4".format(yser, Iser))
        print(" sigc = {:.2f} MPa < ? < {:.2f} MPa = {:.1f} fck".format(sigc, k * fck, k))
        if (sigc > k * fck): print(" ----- PB -------")
        print(" sigs = {0:.2f} MPa < ? < {:.2f} MPa = 0.8 fyk".format(sigs, 0.8 * fyk))
        if (sigs > 0.8 * fyk): print(" ----- PB -------")
        print(" sigs' = {:.2f} MPa".format(sigst))
    return [alphae, yser, Iser, sigc, sigs, sigst]

def MfissTe(As, Asp, beff, bw, hf, h, d, dp, phi, fck, aff = False):
    """moment de fissuration pour la section en té
    entrée: As, Asp :[m²] bw,h,d,dp:[m] phi:[] sortie: [m², m, m, m4, MN.m]"""
    alphae = CST.ES / MAT.Ecm(fck) * (1. + phi / 1.05)
    Ach = bw * h + (beff- bw) * hf + alphae * (As + Asp)
    v = (bw * h**2.0 / 2.0 + (beff - bw) * hf**2.0 / 2.0 + alphae * (As * d + Asp * dp)) / Ach
    vp = h - v
    Ich = bw * h**3 / 3. + (beff - bw) * hf**3. / 3.  \
          - Ach * v**2.0 \
          + alphae * As * d**2.  \
          + alphae * Asp * dp**2.
    fcteff1 = MAT.fctm(fck)
    Mfiss1 = fcteff1 * Ich / vp
    Mfiss2 = fcteff1 * Ich / v
    if (aff):
        print("alphae = {:.3f}, fctm = {:.3f} MPa".format(alphae, fcteff1))
        print("Ach = {:.3f} m², v = {:.3f} m, v' = {:.3f} m, Ich = {:.6f} m4".format(Ach, v, vp, Ich))
        print("M > 0 : Mfiss = {:.3f} MN.m".format(Mfiss1))
        print("M < 0 : Mfiss = {:.3f} MN.m".format(Mfiss2))
    return [Ach, v, vp, Ich, Mfiss1, Mfiss2]
 
#### fluage non linéaire
def phiNL(sigc, phi, fck, t0, typeCiment):
    """  coefficient de fluage non linéaire du béton
        entrée: sigc, fck [MPa], phi, typeCiment [], t0 [j]
    sortie : []"""
    fck0 = MAT.fckt(t0, typeCiment, fck)
    if (sigc < 0.45 * fck0):
        return phi
    else:
        ksig = sigc / fck0 
        ksig=0.45 #essai pour retrouver la solution linéaire
        return phi * exp(1.5 * (ksig - 0.45))

def equationsPhiNL(x, bw, d, dp, As, Asp, phi, t0, typeCiment, fck, fyk, MEd):
    """ équations d'équilibre aux ELS
    entrée : x [MPa,m], bw, d, dp, [m], As, Asp [m²] to [j] typeCiment [],
    fck, fyk [MN.m] MEd [MN.m]
    sortie [m3, MN.m2]"""
    sigc=x[0]
    y=x[1]    
    alphae = CST.ES / MAT.Ecmt(t0, typeCiment, fck) * \
             (1. + phiNL(sigc, phi, fck, t0, typeCiment))  
    eq1 = bw * y**2. / 2 + alphae * (As + Asp) * y - alphae * (d * As + dp * Asp)
    eq2 = MEd * y - sigc * (bw * y**3. / 3. + alphae * As * (d - y)**2. 
                         + alphae * Asp * (y - dp)**2.)
    return [eq1,eq2]


if __name__ == "__main__":
    import EC2.dispositionsconstructives as AC
    print("Vérification des contraintes")
    bw, h = 250e-3, 1000e-3
    fck, fyk = 20., 500.
    phi = 2.
    As = AC.HA(6, 25)
    Asp = AC.HA(3, 12) + AC.HA(3, 8)
    dp, d = 67e-3, 917e-3
    print("As = {0:.0f} mm², As' = {1:.0f} mm², fck = {2:.0f} MPa".
          format(As * 1e6, Asp * 1e6, fck))    
    Mg, Mq = 0.333, 0.167
    psi2 = 0.3
    MEdc = Mg + Mq
    MEdqp = Mg + psi2 * Mq
    phic = MEdqp / MEdc * phi
    print("Etude en caractéristique : MEdc = {0:.3f} MN.m".format(MEdc))
    [Achc, vc, vpc, Ichc, Mfissc1, Mfissc2] = \
                    MfissRect(As, Asp, bw, h, d, dp, 
                              phic, fck, True)
    [alfc, yc, Ic, sigc_c, sigs_c, sigst_c] = \
                    VerifContRect(MEdc, As, Asp, bw, h, d, dp,
                                  fck, fyk, phic, 0.6, True)
    MRdc1 = MRdc(fck, fyk, d, Ic, yc, alfc, True)
    
    phiqp = phi
    print("Etude en quasi-permanente : MEdqp = {0:.3f} MN.m".format(MEdqp))
    [Achqp, vqp, vpqp, Ichqp, Mfissqp1, Mfissqp2] = \
                    MfissRect(As, Asp, bw, h, d, dp, 
                              phiqp, fck, True)
    [alfqp, yqp, Iqp, sigc_qp, sigs_qp, sigst_qp] = \
                    VerifContRect(MEdqp, As, Asp, bw, h, d, dp, 
                                  fck, fyk, phiqp, 0.45, True)
    MRdqp1 = MRdqp(fck, Iqp, yqp, True)
    ### test fluage non linéaire
    print("Résolution du problème du fluage non-linéaire")
    bw = 0.250 #m largeur de la semelle
    d = .917 #m position du centre de gravité des aciers tendus
    As = 2945e-6 #m² section aciers tendus
    dp = 0.067 #m position du centre de gravité des aciers comprimés
    Asp = 490e-6 #m² section aciers comprimés
    phi = 2. #coefficient de fluage initial
    fck = 20. #MPa, résistance du béton en compression
    typeCiment = "N" #s=0.25  #ciment classe normale N
    fyk = 500.  #MPa résistance de l'acier
    MEdqp=0.586 #MN.m moment quasi permanent
    MEdc = 0.5 #MN.m moment caractéristique
    phiqp = phi #coefficient de fluage quasi permanent
    t0 = 15. #28. #j date du chargement du béton
    
    #analyse en quasi permanent
    MEd = MEdqp
    phi = phiqp
    NSol =  fsolve(equationsPhiNL, [5.,0.5], 
                   args=(bw, d, dp, As, Asp, phi, t0, typeCiment, fck, fyk, MEd))
    Nsigc = NSol[0]
    y = NSol[1]
    fckt1 = MAT.fckt(t0, typeCiment, fck)
    Ecmt1 = MAT.Ecmt(t0, typeCiment, fck)
    phiNL1 = phiNL(Nsigc, phi, fck, t0, typeCiment)
    print("Contrainte dans le béton : {:.3f} MPa <?< {:.3f} = 0.45 * {:.3f}" 
            .format(Nsigc, 0.45 * fckt1, fckt1))
    print("Position de l'axe neutre : {:.3f} m".format(y))
    print("Coefficient d'équivalence alphae : {:.3f}".format(
            CST.ES /  Ecmt1 * (1. + phiNL1)))
    print("Coefficient de fluage : {:.3f}".format(phiNL1))

