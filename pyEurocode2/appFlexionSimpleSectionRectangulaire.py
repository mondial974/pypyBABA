from scipy.optimize import fsolve

from corematacierarmature import *
from corematbetonarme import *
from coreconstante import ES, ECU3
from coresituationprojet import *
from utilsprint import *
from utilsmath import racinepolynome3

import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')


class FlexionSimpleSectionRectangulaire():

    def __init__(self, beton, acier, bw, h, c1, c2, Mu, Mser, As2imposee):
        self.beton = beton
        self.acier = acier
        self.bw = bw
        self.h = h
        self.c1 = c1
        self.c2 = c2
        self.Mu = Mu
        self.Mser = Mser
        self.As2imposee = As2imposee

###############################################################################
# HYPOTHESES GENERALES
# Béton : diagramme rectangle simplifié
# Acier : diagramme palier horizontal
###############################################################################

###############################################################################
# DEFINITION DES IS
###############################################################################
    def isaciercomprime(self):
        if self.mucu() > self.mulimite():
            return True
        else:
            return False

###############################################################################
# GEOMETRIE POUTRE
###############################################################################
    def d(self):
        """Calcul la hauteur utile"""
        h = self.h
        c1 = self.c1
        return h - c1

    def dprime(self):
        """Calcul de d'"""
        c2 = self.c2
        return c2

    def deltaprime(self):
        d = self.d()
        dprime = self.dprime()
        return dprime / d


###############################################################################
# RATIO ELU / ELS
###############################################################################


    def gamma(self):
        """Calcul ratio des moments Mu/Mser"""
        Mu = self.Mu
        Mser = self.Mser
        return Mu / Mser


###############################################################################
# MOMENTS REDUITS
###############################################################################


    def mulu(self):
        """Calcul le moment reduit limite ultime"""
        fyd = self.acier.fyd()
        fcd = self.beton.fcd()
        eta = self.beton.eta()
        lmbda = self.beton.lmbda()
        ae = self.beton.ae
        gamma = self.gamma()
        Scbar = self.beton.Scbar()

        a = 3.75 * fyd**2. - 5. * ae**2. * eta * fcd * gamma * Scbar
        b = 25. * ae**2. * eta * fcd * gamma * Scbar + 15. * ae * eta * fcd * fyd
        c = -35. * ae**2. * eta * fcd * gamma * Scbar - 15. * ae * eta * fcd * fyd
        d = 15. * ae**2. * eta * fcd * gamma * Scbar

        a1 = racinepolynome3(a, b, c, d, 0)
        au = a1**2. / (2. * ae * lmbda * eta * (1. - a1)) * fyd / fcd

        mulu = lmbda * au * (1. - lmbda / 2. * au)
        return round(mulu, 4)

    def muls(self):
        """Calcul le moment reduit reduit limite de service"""
        ecu2 = 3.5 / 1000
        fyd = self.acier.fyd()
        Es = ES
        lmbda = self.beton.lmbda()
        ase = ecu2 / (ecu2 + fyd / Es)

        muls = lmbda * ase * (1. - lmbda / 2. * ase)
        return round(muls, 4)

    def mulimite(self):
        """Calcul le moment réduit limite"""
        mulu = self.mulu()
        muls = self.muls()
        return min(mulu, muls)

    def mucu(self):
        """Calcul le moment reduit sollicitant ELU"""
        Mu = self.Mu
        bw = self.bw
        d = self.d()
        fcd = self.beton.fcd()
        return Mu / (bw * d**2 * fcd)


###############################################################################
# CALCUL DES ACIERS : SECTION RECTANGULAIRE SANS ACIERS COMPRIMES
###############################################################################


    def alpha_u(self):
        lmbda = self.beton.lmbda()
        mucu = self.mucu()
        return 1 / lmbda * (1 - sqrt(1 - 2 * mucu))

    def es1(self):
        ecu3 = ECU3
        alpha_u = self.alpha_u()
        return ecu3 * (1 - alpha_u) / alpha_u

    def Ss1(self):
        es1 = self.es1()
        SsPH = self.acier.Ss_PH(es1)
        return SsPH

    def zc(self):
        d = self.d()
        lmbda = self.beton.lmbda()
        alpha_u = self.alpha_u()
        return d * (1. - lmbda / 2. * alpha_u)

    def As1_sac(self):
        MEd = self.Mu
        zc = self.zc()
        Ss1 = self.Ss1()
        return MEd / (zc * Ss1)

###############################################################################
# CALCUL DES ACIERS : SECTION RECTANGULAIRE AVEC ACIERS COMPRIMES
# + COMPRESSION DU BETON LIMITE
###############################################################################

# ACIERS COMPRIMES NON IMPOSES
    def Mlu(self):
        ulu = self.mulimite()
        b = self.bw
        d = self.d()
        fcd = self.beton.fcd()
        return ulu * b * d**2 * fcd

    def Ss1e(self):
        ae = self.beton.ae
        fck = self.beton.fck()
        gamma = self.gamma()
        A = 0.5 / ae + 13
        B = 6517 / ae + 1
        return (A * fck + B) - 0.6 * ae * gamma * fck

    def Ss2e(self):
        ae = self.beton.ae
        fck = self.beton.fck()
        gamma = self.gamma()
        deltaprime = self.deltaprime()
        A = 0.5 / ae + 13
        B = 6517 / ae + 1
        return 0.6 * ae * gamma * fck - deltaprime * (A * fck + B)

    def As2_aac_acni(self):
        MEd = self.Mu
        Mlu = self.Mlu()
        d = self.d()
        dprime = self.dprime()
        Ss2e = self.Ss2e()
        return (MEd - Mlu) / (Ss2e * (d - dprime))

    def As1_aac_acni(self):
        Mlu = self.Mlu()
        zc = self.zc()
        Ss1 = self.Ss1()
        As2 = self.As2_aac_acni()
        Ss2e = self.Ss2e()
        Ss1e = self.Ss1e()
        return Mlu / (zc * Ss1) + As2 * Ss2e / Ss1e

# ACIERS COMPRIMES IMPOSES
    def MEd1(self):
        MEd = self.Mu
        As2 = self.As2imposee
        Ss2e = self.Ss2e()
        d = self.d()
        dprime = self.dprime()
        return MEd - As2 * Ss2e * (d - dprime)

    def As1_aac_aci(self):
        MEd1 = self.MEd1()
        zc = self.zc()
        Ss1 = self.Ss1()
        As2 = self.As2impose
        Ss2e = self.Ss2e()
        Ss1e = self.Ss1e()
        return MEd1 / (zc * Ss1) + As2 * Ss2e / Ss1e

###############################################################################
# CALCUL DES ACIERS : SECTION RECTANGULAIRE AVEC ACIERS COMPRIMES
# + COMPRESSION DU BETON NON LIMITE
###############################################################################

# ACIERS COMPRIMES NON IMPOSES
    def alpha1(self):
        lmbda = self.beton.lmbda()
        mulu = self.mulimite()
        return 1 / lmbda * (1 - sqrt(1 - 2 * mulu))

    def es2u(self):
        ecu3 = ECU3
        deltaprime = self.deltaprime()
        alpha1 = self.alpha1()
        return ecu3 * (alpha1 - deltaprime) / alpha1

    def Ss2u(self):
        es = self.es2u()
        return self.acier.Ss_PH(es)

    def As2u(self):
        MEd = self.Mu
        Mlu = self.Mlu()
        d = self.d()
        dprime = self.dprime()
        Ss2u = self
        return (MEd - Mlu) / ((d - dprime) * Ss2u)

    def As1u(self):
        Mlu = self.Mlu()
        MEd = self.Mu
        d = self.d()
        dprime = self.dprime()
        zc = self.zc()
        fyd = self.acier.fyd()
        return Mlu / (zc * fyd) + (MEd - Mlu) / ((d - dprime) * fyd)

# ACIERS COMPRIMES IMPOSES
    def As1(self):
        MEd1 = self.MEd1()
        zc = self.zc()
        fyd = self.acier.fyd()
        As2 = self.As2imposee
        Ss2u = self.Ss2u()
        return MEd1 / (zc * fyd) + As2 * Ss2u / fyd


###############################################################################
# AFFICHAGE DES RESULTATS
###############################################################################


    def resultat_court(self):
        pass

    def resultat_long(self):
        self.resultat_court()
        printligne("Acier comprimé ?", "-", "-", f"{self.isaciercomprime()}")
        printligne("-", "fcd", "-", f"{self.beton.fcd():.4f}")
        printligne("-", "ae", "-", f"{self.beton.ae:.4f}")
        printligne("-", "eta", "-", f"{self.beton.eta():.4f}")
        printligne("-", "Scbar", "-", f"{self.beton.Scbar():.4f}")
        printligne("-", "gamma", "-", f"{self.gamma():.4f}")

        printligne("-", "lambda", "-", f"{self.beton.lmbda():.4f}")
        printligne("-", "fyd", "-", f"{self.acier.fyd():.4f}")

        printligne("-", "mu_cu", "-", f"{self.mucu():.4f}")
        printligne("-", "mu_lu", "-", f"{self.mulu():.4f}")
        printligne("-", "mu_ls", "-", f"{self.muls():.4f}")
        printligne("-", "mu_limite", "-", f"{self.mulimite():.4f}")
        printligne("-", "Sigma_s1", "-", f"{self.Ss1():.0f}")
        printligne("-", "A_s1", "-", f"{self.As1_sac()*1e4:.2f}")


###############################################################################
# TEST
###############################################################################
if __name__ == '__main__':
    nuance = "S500A"
    situation = SituationProjet('Durable')
    beton = BetonArme(situation, classeexposition='XS1', classeresistance="C25/30",
                      acc=1, act=1, age=28, classeciment='N', ae=15, fiinft0=2)
    acier = AcierArmature(
        situation, nuance, diagramme="Palier horizontal", diametre=8)
    fs = FlexionSimpleSectionRectangulaire(
        beton, acier, bw=18/100, h=60/100, c1=5/100, c2=3/100, Mu=22.253/100, Mser=15.895/100, As2imposee=0/1e4)
    fs.resultat_long()
