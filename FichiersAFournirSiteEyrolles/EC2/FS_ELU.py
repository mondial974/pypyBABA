#-*- Encoding: Utf-8 -*-

import EC2.constantes as CST
import EC2.materiaux as MAT
from scipy.optimize import fsolve

############################
### SECTION RECTANGULAIRE
###########################

#FONCTION DE NIVEAU 2 pour les résultats intermédiaires
def alphase(fck, fyk):
    """ hauteur de réduite de béton comprimé passant par epscu2 et début zone élastique acier 
        entree: fyk:MPa, fck:MPa, 
        sortie:[]
    """
    epscu2 = MAT.epsiloncu2(fck) #déformation limite du béton en parabole rectangle
    epse = MAT.fyd(fyk) / CST.ES  #déformation élastique de l#acier
    return epscu2 / (epscu2 + epse)


def mured(alpha, fck):
    """ moment reduit fonction de alpha
        entree: alpha:[], fck:MPa, 
        sortie:[]
    """
    lambdaR1 = MAT.lambdaR(fck)
    return MAT.eta(fck) * lambdaR1 * alpha * (1. - lambdaR1 * alpha / 2.)


def alphau(mucu, fck,  fyk):
    """hauteur relative de béton comprimé aux ELU : xu/d
        entree: [], sortie:[]
    """
    eta1 = MAT.eta(fck)
    alphase1 = alphase(fck, fyk)
    muse1 = mured(alphase1, fck)
    if (mucu <= muse1): #pas d#aciers comprimés
        if (mucu < eta1 / 2.):
            return (1.0 - (1.0 - 2.0 * mucu / eta1)**0.5) / MAT.lambdaR(fck) #pour fck<50, on retrouve le classique 1,25(1-(1-2mub)**0,5
        else:
            print("muc > eta/2, problème")
            return 0.0
    else: #aciers comprimés né
        return alphase1 #diagramme de déformation figée à la zone élastique

def zu(d, alphaud, fck):
    """ bras de levier pour le calcul des aciers
    """
    return d * (1. - MAT.lambdaR(fck) * alphaud / 2.)


#FONCTION DE NIVEAU 1 pour le résultat définitif
def AsRectELU(MEdu, bw, d, dp, fck, fyk, aff = False):
    """Diagramme de contrainte pour l#acier sans pivot A...
    section d'acier tendu aux ELU sans tenir compte des ELS
    entrée : Mu:MN.m bw:m d:m d#:m fcd:MPa, fyd:MPa, aff:False 
    sortie : Au, A'u :m²
    """
    if (aff): print("Section rectangulaire (sans Asmin)")
    fcd1 = MAT.fcd(fck)
    fyd1 = MAT.fyd(fyk)
    mucu = MEdu / (bw * d**2 * fcd1)
    alphase1 = alphase(fck, fyk)
    muse1 = mured(alphase1, fck)
    if (mucu <= muse1): #pas d#aciers comprimés
        alpha = alphau(mucu, fck, fyk)
        Asu = MEdu / (d * (1. - MAT.lambdaR(fck) * alpha / 2.) * fyd1)
        if (aff):
            print("MEdu = {0:.3f} -> mucu = {1:.4f}, alphacu = {2:.3f} zcu = {3:.3f} m"
                     .format(MEdu, mucu, alpha, zu(d, alpha, fck)))
            print(" -> As >= {0:.1f} mm² As' >= {1:.1f} mm²".format(Asu * 1e6, 0.))
            
        return [Asu, 0] #m²
    else: #aciers comprimés nécessaires
        alpha = alphase1 #diagramme de déformation figée à la zone élastique
        yu = alpha*d
        epsc = MAT.epsiloncu2(fck) * (yu - dp) / yu
        sigsc = min(fyd1, CST.ES  *epsc) #formule sans limitation des contraintes
        MEdu1 = bw * d * d * fcd1 * mured(alpha, fck)
        A1 = (MEdu - MEdu1) / (d - dp) / sigsc #m²
        Asu = MEdu1 / zu(d, alpha, fck) / fyd1 + A1 * sigsc / fyd1
        if (aff):
            print("Aciers comprimés utiles")
            print("MEdu = {:.3f} -> mucu = {:.4f}".format(MEdu, mucu))
            print("muse = {:.4f}, alphase = {:.3f}".format(muse1, alphase1))
            print("epsP = {:.3f} % sigsP = {:.2f} MPa, mulu = {:.3f} MN.m".format(epsc * 1e2, sigsc, MEdu1))
            print(" -> As >= {:.1f} mm² As' >= {:.1f} mm²".format(Asu * 1e6, A1 * 1e6))
        return [Asu, A1]
      
def MRduRect(As, Asp, bw, d, dp, fck, fyk, aff = False):
    """ moment résistant béton aux ELU """
    fyd1 = MAT.fyd(fyk)
    fcd1 = MAT.fcd(fck)
    if (abs(As - Asp) < 1e-9): 
        yu = (1. - .9999) * As  * fyd1 / (0.8 * bw * fcd1)
    else:
        yu = (As - Asp) * fyd1 / (0.8 * bw * fcd1)
    if (aff):
        print(" Départ : ycu = {0:.3f} m".format(yu))
    epsp = MAT.epsiloncu2(fck) * (yu - dp) / yu
    if (epsp >= fyd1 / CST.ES):
        if (aff):  print(" Plastique : yu = {0:.3f} m".format(yu))
        sigsp = fyd1
    else:
        def eq(x):
            return 0.8 * bw * fcd1 * x**2.0 \
                + (Asp * CST.ES * MAT.epsiloncu2(fck) - As * fyd1) * x \
                - Asp * CST.ES * MAT.epsiloncu2(fck) * dp
        yu = fsolve(eq, 0.5)[0]
        if (aff):
            print(" Elastique : ycu = {0:.3f} m".format(yu))
        if (abs(yu) <= 1e-6):
            sigsp = 0.0
        else:
            sigsp = CST.ES * MAT.epsiloncu2(fck) * (yu - dp) / yu
    MRdu1 = 0.8 * bw * yu * fcd1 * (d - 0.4 * yu) + Asp * sigsp * (d - dp) 
    if (aff):
        print(" sigmasp = {0:.3f} MPa".format(sigsp))
        print(" MRdu = {0:.3f} MN.m".format(MRdu1))        
    return MRdu1
	
def AsRectXSDF(MEdu,  MEdc, MEdqp, bw, d, dp, fck, fyk, phi, k1, aff = False, aff2 = False):
    """Diagramme de contrainte pour l'acier sans pivot A...
    section d'acier tendu aux ELU en tenant compte des ELS
    entrée : MEdu,MEdc,MEdqp:MN.m Psi2:[] bw:m d:m d#:m fcd:MPa, fyd:MPa, phi:[], sortie : Au:m²
    rem si l#on veut k1=0,6 (sous c), on donne toutes les valeurs de MEdu,MEdc,MEdqp
    rem si l#on veut k1=0,45 (sous qp), on donne MEdu,MEdqp,MEdqp, 
    """
    gamma = MEdu / MEdc
    phieff = phi * MEdqp / MEdc / 1.05
    fcd1 = MAT.fcd(fck)
    fyd1 = MAT.fyd(fyk)
    mucu = MEdu / (bw * d * d * fcd1)
    #alphase1 = alphase(fck, fyk)
    #muse1 = mured(alphase1, fck)
    mulu1 = mulu(gamma, fck, fyk, phieff, k1, aff2)
    if (mucu <= mulu1): #pas d#aciers comprimés
        alpha = alphau(mucu, fck, fyk)
        As = MEdu / (d * (1. - MAT.lambdaR(fck) * alpha / 2.) * fyd1)
        if (aff):
            print("Section rectangulaire (sans Asmin)")
            print("MEdu = {0:.3f} MN.m -> µcu = {1:.4f} alphacu = {2:.3f} zcu = {3:.3f} m"
                     .format(MEdu, mucu, alpha, zu(d, alpha, fck)))            
            print(" -> As >= {0:.1f} mm² As' >= {1:.1f} mm²".format(As * 1e6, 0.))
        return [As, 0] #m²
    else: #aciers comprimés nécessaires
        mu1 = mulu1 * CST.ALPHAC / (gamma * k1 * CST.GAMMAC)
        alpha1 = 3. / 2. * (1. - (1. - 8 * mu1 / 3)**0.5)
        alphae = CST.ES / MAT.Ecm(fck) * (1 + phieff) #coefficient d#équivalence
        y1 = alpha1 * d
        #calcul ELS
        sigscser = alphae * k1 * fck * (y1 - dp) / y1 #aciers comprimés
        sigsser = alphae * k1 * fck * (d - y1) / y1   #aciers tendus
        #calcul ELU
        alpha = alphalu(mulu1, fck) #diagramme de déformation figée à µlu
        yu = alpha * d
        epsc = MAT.epsiloncu2(fck) * (yu - dp) / yu
        sigsc = min(fyd1, CST.ES * epsc) #formule sans limitation des contraintes
        #contrainte équivalente
        sigsce = min(sigsc, gamma * sigscser)
        sigse = min(fyd1, gamma * sigsser)
        MEdu1 = bw * d * d * fcd1 * mured(alpha, fck)
        if (MEdu1 < 0.6 * MEdu):
            print("Mlu < 0.6*Medu")
        Asp = (MEdu - MEdu1) / (d - dp) / sigsce #m²
        As = MEdu1 / zu(d, alpha, fck) / fyd1 + Asp * sigsce / sigse
        if (aff):
            print("Section rectangulaire (sans Asmin)")
            print("MEdu = {:.3f} MN.m  µcu = {:.4f} alphacL = {:.3f} alphae = {:.3f}"
                     .format(MEdu, mucu, alpha1, alphae))
            print("y1 = {:.3f} m sigsc = {:.1f} MPa sigsc' = {:.1f} MPa"
                     .format(y1, sigsser, sigscser))
            print("yu = {:.3f} m sigs' = {:.1f} MPa zlu = {:.3f} m"
                     .format(yu, sigsc, zu(d, alpha, fck)))
            print("sigse = {:.1f} MPa sigse' = {:.1f} MPa".format(sigse, sigsce))            
            print("As > {:.1f} mm², As' > {:.1f} mm²".format(As * 1e6, Asp * 1e6))
        return [As, Asp]
    

def alphalu(mulu, fck):
    return (1.0 - (1.0 - 2.0 * mulu / MAT.eta(fck) )**0.5)/ MAT.lambdaR(fck)


def mulu(gamma, fck,  fyk, phi, k, aff = False):
    """valeur de mulu aux ELU/ELS
    entrée : gamma [], fck, fyk [Mpa], phi, k []
    """
    def solve3deg(a, b, c, d):
        def f(x, a, b, c, d):
            return a * x**3.0 + b * x**2.0 + c * x + d
        return fsolve(f, 0.2, args=(a, b, c, d))[0]    
    fyd1, fcd1 = MAT.fyd(fyk), MAT.fcd(fck)
    eta1, lambdaR1  = MAT.eta(fck), MAT.lambdaR(fck) 
    alphae = CST.ES / MAT.Ecm(fck)*( 1. + phi)
    sigbc = k * fck
    a = 3.75 * fyd1**2 - 5. * alphae**2 * eta1 * fcd1 * gamma * sigbc
    b = 25. * alphae**2 * eta1 * fcd1 * gamma * sigbc + 15. * alphae * eta1 * fcd1 * fyd1
    c = - 35. * alphae**2 * eta1 * fcd1 * gamma * sigbc - 15. * alphae * eta1 * fcd1 * fyd1
    d = 15. * alphae**2 * eta1 * fcd1 * gamma * sigbc
    alpha1 = solve3deg(a, b, c, d) 
    alphau = alpha1**2 / (2. * alphae * (1 - alpha1) * lambdaR1 * eta1) * fyd1 / fcd1 
    mulu = lambdaR1 * alphau * (1 - lambdaR1 / 2 * alphau)
    alphase1 = alphase(fck, fyk)
    muse1 = mured(alphase1, fck)
    mulu1 = min(mulu, muse1)
    if (aff):
        print(" Calcul du µlu : détails")
        print("  -- gamma = {0:.3f}".format(gamma))
        print("  -- lambda = {0:.3f} phieff = {1:.4f} alphae = {2:.3f} sigc = {3:.1f} MPa".format(lambdaR1, phi, alphae, sigbc))
        print("  -- a = {} b = {} c = {} d = {}".format(a, b, c, d))
        mu1 = mulu1 * CST.ALPHAC / (gamma * k * CST.GAMMAC)
        print("  -- alpha1 = {0:.4f} µ1 = {1:.4f} alphalu = {2:.4f} µlu = {3:.4f} µse = {4:.4f}".format(
                alpha1, mu1, alphau, mulu, muse1))
        print("  -> µlu = {0:.4f}".format(mulu1)) 
    return mulu1

def MTu(beff1, hf, d,  fck, aff = False):
    """ Moment de réference pour la section en Té
    entrée : beff, hf, d, [m] fck [MPa]
    sortie : [MN.m]"""
    MTu1 = beff1 * hf * (d - hf / 2) * MAT.fcd(fck)
    if (aff):
        print("Mtu = {0:.3f} MN.m".format(MTu1))
    return MTu1

def AsTeELU(MEdu, bw, beff1, h, hf,  d, dp,  fck, fyk, aff = False):
    """Dimensionnement des sections d'aciers aux ELU pour la section en Té
    entrée : MEdu [MN.m] bw, beff, h, hf,  d, dp [m] fck, fyk [MPa] 
    sortie : [m²]"""
    if (aff): print("Section en té (sans Asmin)")
    MTu1 = MTu(beff1, hf, d, fck, aff)
    if (MEdu <= MTu1): #dimensionnement en section rectangulaire (bw=beff)
        return AsRectELU(MEdu, beff1, d, dp, fck, fyk, aff)
    else:
        MEdu1 = MEdu - MTu1 * (beff1 - bw) / beff1
        #Mu2 = Mu - Mu1
        fcd1 = MAT.fcd(fck)
        fyd1 = MAT.fyd(fyk)
        mucu1 = MEdu1 / (bw * d * d * fcd1)
        alphase1 = alphase(fck, fyk)
        muse1 = mured(alphase1, fck)
        if (aff):
            print(" MEdu = {3:.3f} MN.m MEdu1 = {0:.3f} MN.m, mucu1 = {1:.3f} muse1 = {2:.3f}" \
                  .format(MEdu1, mucu1, muse1, MEdu))
        if (mucu1 <= muse1): #pas d#aciers comprimés
            alphacu1 = alphau(mucu1, fck, fyk)
            zcu1 = d * (1.-MAT.lambdaR(fck) * alphacu1 / 2.)
            As = MEdu1 / (zcu1 * fyd1) + (beff1 - bw) * hf * fcd1 / fyd1
            if (aff):
                print(" alphacu1 = {0:.3f} zcu1 = {1:.3f} m\nAs = {2:.3f} mm² As' = 0 mm²" \
                      .format(alphacu1, zcu1, As * 1e6))
            return [As, 0.0] #m²
        else: #aciers comprimés nécessaires
            alpha = alphase1 #diagramme de déformation figée à la zone élastique
            yu = alpha * d
            epsc = MAT.epsiloncu2(fck) * (yu - dp) / yu
            sigsc = min(fyd1, CST.ES * epsc) #formule sans limitation des contraintes
            Musl = bw * d * d * fcd1 * mured(alpha, fck)
            A1 = (MEdu1 - Musl) / (d - dp) / sigsc #m²
            As = Musl / zu(d, alpha, fck) / fyd1 + A1 * sigsc / fyd1 \
            + (beff1 - bw) * hf * fcd1 / fyd1
            print(" Mse = {0:.3f} MN.m zce = {1:.3f} m eps' = {2:.3f} % sig' = {3:.2f} MPa" \
                  .format(Musl, zu(d, alpha, fck), epsc *100, sigsc))
            print("As = {0:.3f} mm² As' = {1:.3f} mm²".format(As * 1e6, A1 * 1e6))
            return [As, A1] #m²
	  
def MRduTe(As, Asp, beff1, bw, hf, d, dp, fck, fyk, aff = False):
    """ moment résistant béton aux ELU 
    entrée : As, Asp [m2], bw, hf, d, dp [m], fck, fyk [MPa]
    sortie : [MN.m]"""
    fyd1 = MAT.fyd(fyk)
    fcd1 = MAT.fcd(fck)
    yu = (As - Asp) * fyd1 / (0.8 * beff1 * fcd1)
    if (aff):
        print(" Départ : ycu = {0:.3f} m".format(yu))
    if (0.8 * yu < hf): #caclul en section rectangulaire de largeur beff
        if (aff): print(" Section rectangulaire")
        return MRduRect(As, Asp, beff1, d, dp, fck, fyk, aff)
    yu = ((As - Asp) * fyd1 - (beff1 - bw) * hf * fcd1) / (0.8 * bw * fcd1)
    epsp = MAT.epsiloncu2(fck) * (yu - dp) / yu
    if (epsp >= fyd1 / CST.ES):
        if (aff):  print(" Plastique : yu = {0:.3f} m".format(yu))
        sigsp = fyd1
    else:
        def eq(x):
            return 0.8 * bw * fcd1 * x**2.0 \
                + (Asp * CST.ES * MAT.epsiloncu2(fck) - As * fyd1  \
                   (beff1 - bw) * hf * fcd1) * x \
                - Asp * CST.ES * MAT.epsiloncu2(fck) * dp
        yu = fsolve(eq, 0.5)[0]
        if (aff):
            print(" Elastique : ycu = {0:.3f} m".format(yu))
        if (abs(yu) <= 1e-6):
            sigsp = 0.0
        else:
            sigsp = CST.ES * MAT.epsiloncu2(fck) * (yu - dp) / yu
    MRdu1 = 0.8 * bw * yu * fcd1 * (d - 0.4 * yu)  \
          + Asp * sigsp * (d - dp)                 \
          + (beff1 - bw) * hf * fcd1 * (d - hf / 2.)
    if (aff):
        print(" sigmasp = {0:.3f} MPa".format(sigsp))
        print(" MRdu = {0:.3f} MN.m".format(MRdu1))        
    return MRdu1


def alphauTe(Mu, bw, beff, h, ho, d, dp,  fck, fyk):
    """hauteur relative de béton comprimé aux ELU : xu/d
    entree: [], sortie:[]"""
    MTu1 = MTu(beff,ho,d,fck)
    if (Mu<= MTu1): #dimensionnement en section rectangulaire (bw = beff)
        mub = Mu / beff / d / d / MAT.fcd(fck)
        return alphau(mub, fck, fyk)
    else:
        Mu1 = Mu-MTu1*(beff-bw)/beff
        #Mu2 = Mu-Mu1
        fcd1 = MAT.fcd(fck)
        #fyd1 = MAT.fyd(fyk)
        mubu1 = Mu1/(bw*d*d*fcd1)
        alphase1 = alphase(fck, fyk)
        muse1 = mured(alphase1,fck)
        if (mubu1<=muse1): #pas d#aciers comprimés
            return alphau(mubu1, fck, fyk)
        else: #aciers comprimés nécessaires
            return alphase1 #diagramme de déformation figée à la zone élastique
	  

def beff(bw, b1, b2, lo, aff = False):
    """ largeur efficace [5.3.2.1]
    entrée : bw, b1, b2, lo [m]
    sortie : [m]"""
    beff1 = min(0.2 * b1 + 0.1 * lo, min(.2 * lo, b1))
    beff2 = min(0.2 * b2 + 0.1 * lo, min(.2 * lo, b2))
    if (aff):
        print("beff1 = min(0.2 * b1 + 0.1 * lo, min(.2 * lo, b1)\n      = min({0:.3f}, min({1:.3f}, {2:.3f})) = {3:.3f} m" \
                           .format(0.2 * b1 + 0.1 * lo, .2 * lo, b1, beff1))
        print("beff2 = min(0.2 * b2 + 0.1 * lo, min(.2 * lo, b2)\n      = min({0:.3f}, min({1:.3f}, {2:.3f})) = {3:.3f} m" \
                           .format(0.2 * b2 + 0.1 * lo, .2 * lo, b2, beff2))
        temp = bw + 2. * min(min(beff1, beff2), min(b1, b2))
        print("beff = min(2.0 * min(beff1, beff2) + bw, b1 + b2 + bw)\n     = 2. min({0:.3f}, {1:.3f}) + {2:.3f})) = {4:.3f} m" \
                           .format(beff1, beff2, bw, b1 + b2 + bw, temp))
    return bw + 2. * min(min(beff1, beff2), min(b1, b2))
    #beff=min(beff1+beff2+bw,b)


def PhiEff(phi, gamma, psi2):
    """retourne l'expression du coefficient de fluage en fonction de MEd,qp/MEd,c calculé à partir de Phi_infty"""
    return phi * (1.5 - psi2 * 1.35 + gamma * (psi2 - 1))/(1.5 - 1.35)

def AsmaxRect(bw, h, aff = False):
    """Section maximale pour la section rectangulaire hors recouvrement
    entrée : bw, h:m 
    sortie : m²"""
    Ac = bw * h
    Asmax = 0.04 * Ac
    if (aff):
        print("Asmax section rectangulaire\nAsmax = 0.04 Ac = 0.04 * {0:.3f} = {1:.3f} mm²".format(Ac, 0.04 * Ac * 1e6))
    return Asmax

def AsminRect(bw, d, fck, fyk, aff = False):
    """Section maximale pour la section rectangulaire hors recouvrement
    entrée : bw, h:m 
    sortie : m²"""
    Asmin = 0.26 * bw  * d * MAT.fctm(fck) / fyk
    #Asmin2 = 0.0013 * bw * d
    #Asmin = max(Asmin1, Asmin2)
    if (aff):
#        print("Section rectangulaire\nAsmin = {2:.3f} mm² = max(0.26 fctm / fyk, 0.0013) bw d = max ({0:.3f}, {1:.3f})" \
#              .format(Asmin1 *1e6, Asmin2 * 1e6, Asmin * 1e6))
        print("Asmin section rectangulaire\nAsmin = 0.26 fctm / fyk bw d = {0:.3f} mm²" \
              .format(Asmin * 1e6))
        print(" fctm = {0:.3f} MPa".format(MAT.fctm(fck)))
    return Asmin


def AsmaxTe(bw, h, beff, hf, aff = False):
    """Section maximale pour la section rectangulaire hors recouvrement
    entrée : bw, h:m 
    sortie : m²"""
    Ac = beff * hf + (h -hf) * bw
    Asmax = 0.04 * Ac
    if (aff):
        print("Asmax section en té\nAsmax = 0.04 Ac = 0.04 * {0:.3f} = {1:.3f}".format(Ac, Asmax * 1e6))
    return Asmax
    
def AsminTe(bw, h, beff, hf, fck, fyk, aff = False):
    """Section maximale pour la section rectangulaire hors recouvrement
    entrée : bw, h:m 
    sortie : m²"""
    Ac = bw * h + (beff - bw) * hf
    vp = (bw * h**2.0 + (beff- bw) * hf**2.0) / (2.0 * Ac)
    v = h - vp
    Ic = bw * h**3.0 / 3.0 + (beff- bw) * hf**3.0 / 3.0 - Ac * vp**2.0
    Asmin = Ic / (0.81 * h * v) * MAT.fctm(fck) / fyk
    if (aff):
        print("Asmin section en té\nAsmin = Ic / (0.81 h v ) fctm / fyk = {0:.3f} mm²" \
              .format(Asmin * 1e6))
        print(" fcm = {0:.3f} MPa".format(MAT.fctm(fck)))
        print(" Ac = {0:.3f} m² v = {1:.3f} m v' = {2:.3f} m I = {3:.4f} m²".format(Ac, v, vp, Ic))
    return Asmin


def AsRectELU2(MEdu, bw, d, dp, fck, fyk, k, epsilonuk, aff = False):
    """  section d'acier tendue aux ELU sans tenir compte des ELS
    avec diagramme inclinée
    entrée : Mu:MN.m bw:m d:m d#:m fcd:MPa, fyd:MPa, aff:False 
    sortie : As, A's:m² sigs1, sigsc1: MPa
    """
    if (aff): print("Section rectangulaire avec diagramme inclinée pour l'acier (sans Asmin)")
    fcd1 = MAT.fcd(fck)
    fyd1 = MAT.fyd(fyk)
    mucu = MEdu / (bw * d**2 * fcd1)
    alphase1 = alphase(fck, fyk)
    muse1 = mured(alphase1, fck)
    if (mucu <= muse1): #pas d#aciers comprimés
        alpha = alphau(mucu, fck, fyk)
        epscu2, epsud = MAT.epsiloncu2(fck), MAT.epsilonud(epsilonuk)
        alphaAB = epscu2 / (epscu2 + epsud)
        if (alpha < alphaAB): #pivot A
            sigs = MAT.sigmas2(epsud, fyk, k, epsilonuk)
            if (aff): print("Pivot A : eps = {:.3f} % sigs = {:.3f} MPa"
               .format(epsud * 1e2, sigs))
        else:#pivot B
            eps = (1. - alpha) / alpha * epscu2
            sigs = MAT.sigmas2(eps, fyk, k, epsilonuk)    
            if (aff): print("Pivot B : eps = {:.3f} % sigs = {:.3f} MPa"
               .format(eps* 1e2, sigs))
        Asu = MEdu / (d * (1. - MAT.lambdaR(fck) * alpha / 2.) * sigs)
        if (aff):
            print("MEdu = {0:.3f} -> mucu = {1:.4f}, alphacu = {2:.3f} zcu = {3:.3f} m"
                     .format(MEdu, mucu, alpha, zu(d, alpha, fck)))
            print(" -> As >= {0:.1f} mm² As' >= {1:.1f} mm²".format(Asu * 1e6, 0.))
        return [Asu, 0, sigs, 0.] #m²
    else: #aciers comprimés nécessaires
        alpha = alphase1 #diagramme de déformation figée à la zone élastique
        yu = alpha * d
        epsc = MAT.epsiloncu2(fck) * (yu - dp) / yu
        #sigsc = min(fyd1, CST.ES  *epsc) #formule sans limitation des contraintes
        sigsc = MAT.sigmas2(epsc, fyk, k, epsilonuk)
        MEdu1 = bw * d * d * fcd1 * mured(alpha, fck)
        A1 = (MEdu - MEdu1) / (d - dp) / sigsc #m²
        epse = MAT.fyd(fyk) / CST.ES
        sigs = MAT.sigmas2(epse, fyk, k, epsilonuk)
        Asu = MEdu1 / zu(d, alpha, fck) / fyd1 + A1 * sigsc / sigs
        if (aff):
            print("Aciers comprimés utiles")
            print("Limite elastique : eps = {:.3f} % sigs = {:.3f} MPa".
                  format(epse, sigs))
            print("MEdu = {:.3f} -> mucu = {:.4f}".format(MEdu, mucu))
            print("muse = {:.4f}, alphase = {:.3f}".format(muse1, alphase1))
            print("EpsP = {:.5f} SigsP = {:.2f} MPa, Mulu = {:.3f} MN.m".format(epsc, sigsc, MEdu1))
            print(" -> As >= {:.1f} mm² As' >= {:.1f} mm²".format(Asu * 1e6, A1 * 1e6))
        return [Asu, A1, sigs, sigsc]

if __name__ == "__main__":
    bw, h = 0.2, .600
    hf, beff1 = 0.12, 1.1
    d, dp = 0.55, 0.05    
    fck = 25.
    fyk = 500.
    Mg, Mq = .083, 0.155
    MEdu = 1.35 * Mg + 1.5 * Mq
    #section en té
    [As1, Asp1] = AsTeELU(MEdu, bw, beff1, h, hf, d, dp,  fck, fyk, True)
    Asmax1 = AsmaxTe(bw, h, beff1, hf, True)
    Asmin1 = AsminTe(bw, h, beff1, hf, fck, fyk, True)
    #section rectangulaire
    [As2, Asp2 ] = AsRectELU(MEdu, bw, d, dp, fck, fyk, True)
    Asmax2 = AsmaxRect(bw, h, True)
    Asmin2 = AsminRect(bw, d, fck, fyk, True)
    ##" calcul avec branche inclinée
    epsilonuk, k = 5e-2, 1.08
    [As3, Asp3, sigs1, sigsc1 ] = AsRectELU2(MEdu, bw, d, dp, fck, fyk, epsilonuk, k, True)
    ###
    import matplotlib.pylab as plt
    import numpy as np
    plt.close('all')
    plt.figure()
    plt.grid('on')
    eps = np.linspace(0., MAT.epsilonud(epsilonuk) + 0.001, 100)
    sigs1 = np.array([MAT.sigmas1(epsi, fyk) for epsi in eps])
    sigs2 = np.array([MAT.sigmas2(epsi, fyk, k, epsilonuk) for epsi in eps])
    plt.plot( eps * 100, sigs1, 'k')
    plt.plot( eps * 100, sigs2, 'k-')
    plt.xlabel(r'$\epsilon$ [%]')
    plt.ylabel(r'$\sigma_s$ [MPa]')
    plt.title(u"Loi de comportement de l'acier")
    plt.savefig("./images/LCacier.pdf")
    plt.show()    
    plt.grid(True)
   
    plt.figure()
    alpha = np.linspace( 0.001, 1. , 100)
    MEdu = bw * d**2 * MAT.fcd(fck) * np.array([ mured(alphai, fck) for alphai in alpha])
    As1 = np.array([AsRectELU(MEdui, bw, d, dp, fck, fyk) for MEdui in MEdu])
    As2 = np.array([AsRectELU2(MEdui, bw, d, dp, fck, fyk, k, epsilonuk) for MEdui in MEdu])
    plt.plot( alpha * 100, As1[:, 0] * 1e6, 'k')
    plt.plot( alpha * 100, As1[:, 1] * 1e6, 'k')
    plt.plot( alpha * 100, As2[:, 0] * 1e6, 'k--')
    plt.plot( alpha * 100, As2[:, 1] * 1e6, 'k--')
    plt.grid(True)
    plt.xlabel(r'$\alpha$ [%]')
    plt.ylabel(r'$A_s$ [mm$^2$]')
    plt.title(u"Section d'acier en flexion simple")
    plt.savefig("./images/AsFlexSimpleRect.pdf")
    plt.show()
    
    plt.figure()
    plt.grid('on')
    plt.plot( alpha * 100, As2[:, 2], 'k', label = r'$\sigma_s$')
    plt.plot( alpha * 100, As2[:, 3], 'k--', label = r'$\sigma_s^\prime$')
    plt.legend()
    plt.xlabel(r'$\alpha$ [%]')
    plt.ylabel(r'$\sigma_s$ [MPa]')
    plt.title(u"Evolution des contraintes dans la section")
    plt.savefig("./images/SigmasFSRect.pdf")
    plt.show()
    
    ##test pour As = As' en section rectangulaire
    import dispositionsconstructives as DC
    print("Vérification des contraintes")
    bw, h = 250e-3, 1000e-3
    fck, fyk = 20., 500.
    phi = 2.
    As = DC.HA(6, 25)
    Asp = DC.HA(3, 12) + DC.HA(3, 8)
    dp, d = 67e-3, 917e-3
    Asp = As
    MRduRect(As, Asp, bw, d, dp, fck, fyk, True)
