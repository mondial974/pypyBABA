from utilsmath import racinepolynome2
from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *


class VerifContrainteELSSectionRectangulaire:
    def __init__(self, beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2):
        self.beton = beton
        self.acier = acier
        self.Mser = Mser
        self.bw = bw
        self.beff = beff
        self.h = h
        self.hf = hf
        self.c1 = c1
        self.c2 = c2
        self.As1 = As1
        self.As2 = As2

    ###############################################################################
    # Définition des is
    ###############################################################################

    def isSectionTe(self):
        if beff > self.bw:
            return True
        else:
            return False

    def isSectionRect(self):
        if self.beff <= self.bw:
            return True
        else:
            return False

    def isANDansTable(self):
        if self.fhf() > 0:
            return True
        else:
            return False

    # def isSectionRectFissuree(self):
    #     if self.Sct_rect_nonfissuree() > self.beton.fctm():
    #         return True
    #     else:
    #         return False

    # def isContrainteBetonDepassee(self):
    #     if self.Sc() > self.beton.Scbar():
    #         return True
    #     else:
    #         return False

    ###############################################################################
    # Caractéristique géométrique commune section rectangulaire et Té
    ###############################################################################
    def d(self):
        return self.h - self.c1

    def dprime(self):
        return self.c2

    ###############################################################################
    # Caractéristique géométrique section rectangulaire
    ###############################################################################
    #   SECTION RECTANGULAIRE
    def Ach_rect(self):
        bw = self.bw
        h = self.h
        ae = self.beton.ae
        As1 = self.As1
        As2 = self.As2
        return bw * h + ae * (As1 + As2)

    def vprime_rect(self):
        bw = self.bw
        h = self.h
        d = self.d()
        dprime = self.dprime()
        ae = self.beton.ae
        Ach = self.Ach_rect()
        As1 = self.As1
        As2 = self.As2
        return ((bw * h**2) / 2 + ae * (As1 * d + As2 * dprime)) / Ach

    def v_rect(self):
        return self.h - self.vprime_rect()

    #   SECTION EN TE
    def Ach_te(self):
        bw = self.bw
        beff = self.beff
        h = self.h
        hf = self.hf
        ae = self.beton.ae
        As1 = self.As1
        As2 = self.As2
        return bw * h + (beff - bw) * hf + ae * (As1 + As2)

    def vprime_te(self):
        bw = self.bw
        beff = self.beff
        h = self.h
        hf = self.hf
        d = self.d()
        dprime = self.dprime()
        ae = self.beton.ae
        Ach = self.Ach_te()
        As1 = self.As1
        As2 = self.As2
        return (
            bw * h**2 / 2 + (beff - bw) * hf**2 / 2 + ae * (As1 * d + As2 * dprime)
        ) / Ach

    def v_te(self):
        return self.h - self.vprime_te()

    ###############################################################################
    # Contrainte dans la section rectangulaire et en Té non fissurée
    ###############################################################################
    #   SECTION RECTANGULAIRE

    def Ich_rect(self):
        bw = self.bw
        h = self.h
        d = self.d()
        dprime = self.dprime()
        vprime = self.vprime_rect()
        ae = self.beton.ae
        Ach = self.Ach_rect()
        As1 = self.As1
        As2 = self.As2
        return (
            (bw * h**3.0) / 3.0
            + ae * (As1 * d**2.0 + As2 * dprime**2.0)
            - Ach * vprime**2.0
        )

    def Sct_rect_nonfissuree(self):
        Mser = self.Mser
        v = self.v_rect()
        Ich = self.Ich_rect()
        return Mser * v / Ich

    def Sc_rect_nonfissuree(self):
        Mser = self.Mser
        vprime = self.vprime_rect()
        Ich = self.Ich_rect()
        return Mser * vprime / Ich

    def Ss1_rect_nonfissuree(self):
        ae = self.beton.ae
        Mser = self.Mser
        vprime = self.vprime_rect()
        d = self.d()
        Ich = self.Ich_rect()
        return ae * Mser * (d - vprime) / Ich

    def Ss2_rect_nonfissuree(self):
        if self.As2 == 0:
            return 0
        else:
            ae = self.beton.ae
            Mser = self.Mser
            vprime = self.vprime_rect()
            dprime = self.dprime()
            Ich = self.Ich_rect()
            return ae * Mser * (vprime - dprime) / Ich

    #   SECTION EN TE
    def Ich_te(self):
        bw = self.bw
        h = self.h
        hf = self.hf
        d = self.d()
        dprime = self.dprime()
        vprime = self.vprime_te()
        ae = self.beton.ae
        Ach = self.Ach_te()
        As1 = self.As1
        As2 = self.As2
        return (
            bw * h**3 / 3
            + (beff - bw) * hf**3
            + ae * (As1 * d**2 + As2 * dprime**2)
            - Ach * vprime**2
        )

    def Sct_te_nonfissuree(self):
        Mser = self.Mser
        v = self.v_te()
        Ich = self.Ich_te()
        return Mser * v / Ich

    def Sc_te_nonfissuree(self):
        Mser = self.Mser
        vprime = self.vprime_te()
        Ich = self.Ich_te()
        return Mser * vprime / Ich

    def Ss1_te_nonfissuree(self):
        ae = self.beton.ae
        Mser = self.Mser
        vprime = self.vprime_te()
        d = self.d()
        Ich = self.Ich_te()
        return ae * Mser * (d - vprime) / Ich

    def Ss2_te_nonfissuree(self):
        if self.As2 == 0:
            return 0
        else:
            ae = self.beton.ae
            Mser = self.Mser
            vprime = self.vprime_te()
            dprime = self.dprime()
            Ich = self.Ich_te()
            return ae * Mser * (vprime - dprime) / Ich

    ###############################################################################
    # Contrainte dans la section rectangulaire et Té fissurée
    ###############################################################################
    #   SECTION RECTANGULAIRE

    def x1_rect(self):
        bw = self.bw
        d = self.d()
        dprime = self.dprime()
        ae = self.beton.ae
        As1 = self.As1
        As2 = self.As2

        a = bw / 2
        b = ae * (As1 + As2)
        c = -ae * (As1 * d + As2 * dprime)

        return racinepolynome2(a, b, c, 1)

    def Icf_rect(self):
        bw = self.bw
        x1 = self.x1_rect()
        ae = self.beton.ae
        d = self.d()
        dprime = self.dprime()
        As1 = self.As1
        As2 = self.As2
        return (
            bw * x1**3 / 3 + ae * As2 * (x1 - dprime) ** 2 + ae * As1 * (d - x1) ** 2
        )

    def Sc_rect_fissuree(self):
        Mser = self.Mser
        Icf = self.Icf_rect()
        x1 = self.x1_rect()
        return Mser / Icf * x1

    def Ss1_rect_fissuree(self):
        Mser = self.Mser
        ae = self.beton.ae
        d = self.d()
        Icf = self.Icf_rect()
        x1 = self.x1_rect()
        return ae * Mser / Icf * (d - x1)

    def Ss2_rect_fissuree(self):
        if self.As2 == 0:
            return 0
        else:
            Mser = self.Mser
            ae = self.beton.ae
            dprime = self.dprime()
            Icf = self.Icf_rect()
            x1 = self.x1_rect()
            return ae * Mser / Icf * (x1 - dprime)

    #   SECTION EN TE
    def fhf(self):
        beff = self.beff
        hf = self.hf
        ae = self.beton.ae
        As1 = self.As1
        As2 = self.As2
        d = self.d()
        dprime = self.dprime()
        return (
            beff * hf**2 / 2 + ae * (As1 + As2) * hf - ae * (As1 * d + As2 * dprime)
        )

    def x1_te(self):
        if self.isANDansTable():
            # Calcul section rectangulaire largeur beff
            bw = self.beff
            d = self.d()
            dprime = self.dprime()
            ae = self.beton.ae
            As1 = self.As1
            As2 = self.As2
            a = bw / 2
            b = ae * (As1 + As2)
            c = -ae * (As1 * d + As2 * dprime)
            return racinepolynome2(a, b, c, 1)
        else:
            # Calcul section en Te
            bw = self.bw
            beff = self.beff
            hf = self.hf
            d = self.d()
            dprime = self.dprime()
            ae = self.beton.ae
            As1 = self.As1
            As2 = self.As2
            a = bw / 2
            b = (beff - bw) * hf + ae * (As1 + As2)
            c = -((beff - bw) * hf**2 / 2 + ae * (As1 * d + As2 * dprime))
            return racinepolynome2(a, b, c, 1)

    def Icf_te(self):
        if self.isANDansTable():
            # Calcul section rectangulaire largeur beff
            bw = self.beff
            x1 = self.x1_te()
            ae = self.beton.ae
            d = self.d()
            dprime = self.dprime()
            As1 = self.As1
            As2 = self.As2
            return (
                bw * x1**3 / 3
                + ae * As2 * (x1 - dprime) ** 2
                + ae * As1 * (d - x1) ** 2
            )
        else:
            # Calcul section en Te
            bw = self.bw
            beff = self.beff
            hf = self.hf
            x1 = self.x1_te()
            ae = self.beton.ae
            d = self.d()
            dprime = self.dprime()
            As1 = self.As1
            As2 = self.As2
            return (
                beff * x1**3 / 3
                - (beff - bw) * (x1 - hf) ** 3 / 3
                + ae * As2 * (x1 - dprime) ** 2
                + ae * As1 * (d - x1) ** 2
            )

    def Sc_te_fissuree(self):
        Mser = self.Mser
        Icf = self.Icf_te()
        x1 = self.x1_te()
        return Mser / Icf * x1

    def Ss1_te_fissuree(self):
        Mser = self.Mser
        ae = self.beton.ae
        d = self.d()
        Icf = self.Icf_te()
        x1 = self.x1_te()
        return ae * Mser / Icf * (d - x1)

    def Ss2_te_fissuree(self):
        if self.As2 == 0:
            return 0
        else:
            Mser = self.Mser
            ae = self.beton.ae
            dprime = self.dprime()
            Icf = self.Icf_te()
            x1 = self.x1_te()
            return ae * Mser / Icf * (x1 - dprime)

    ###############################################################################
    # Fonctions d'affichage des résultats
    ###############################################################################
    def resultat_long(self):
        if self.isSectionRect():
            self.resultat_long_rect()
        else:
            self.resultat_long_te()

    def resultat_long_rect(self):
        printentete()
        printligne("Section Rectangualire ?", "-", "-", f"{self.isSectionRect()}")
        print("Caractéristique géométrique")
        printligne("-", "Ach", "cm2", f"{self.Ach_rect()*1e4:.2f}")
        printligne("-", "v", "cm", f"{self.vprime_rect()*100:.2f}")
        printligne("-", "v'", "cm", f"{self.v_rect()*100:.2f}")
        print("Section non fissurée")
        printligne("-", "Ich", "cm4", f"{self.Ich_rect():.8f}")
        printligne("-", "Sct", "MPa", f"{self.Sct_rect_nonfissuree():.2f}")
        printligne("-", "Sc", "MPa", f"{self.Sc_rect_nonfissuree():.2f}")
        printligne("-", "Ss1", "MPa", f"{self.Ss1_rect_nonfissuree():.2f}")
        printligne("-", "Ss2", "MPa", f"{self.Ss2_rect_nonfissuree():.2f}")
        print("Section fissurée")
        printligne("-", "x1", "cm", f"{self.x1_rect()*100:.2f}")
        printligne("-", "Icf", "-", f"{self.Icf_rect():.8f}")
        printligne("-", "Sc", "MPa", f"{self.Sc_rect_fissuree():.2f}")
        printligne("-", "Ss1", "MPa", f"{self.Ss1_rect_fissuree():.2f}")
        printligne("-", "Ss2", "MPa", f"{self.Ss2_rect_fissuree():.2f}")

    def resultat_long_te(self):
        printentete()
        printligne("Section en T ?", "-", "-", f"{self.isSectionTe()}")
        printligne("AN dans la table?", "-", "-", f"{self.isANDansTable()}")
        printligne("", "f(hf)", "-", f"{self.fhf()*1e6:.2f}")
        print("Caractéristique géométrique")
        printligne("-", "Ach", "cm2", f"{self.Ach_te()*1e4:.2f}")
        printligne("-", "v", "cm", f"{self.vprime_te()*100:.2f}")
        printligne("-", "v'", "cm", f"{self.v_te()*100:.2f}")
        print("Section non fissurée")
        printligne("-", "Ich", "cm4", f"{self.Ich_te():.8f}")
        printligne("-", "Sct", "MPa", f"{self.Sct_te_nonfissuree():.2f}")
        printligne("-", "Sc", "MPa", f"{self.Sc_te_nonfissuree():.2f}")
        printligne("-", "Ss1", "MPa", f"{self.Ss1_te_nonfissuree():.2f}")
        printligne("-", "Ss2", "MPa", f"{self.Ss2_te_nonfissuree():.2f}")
        print("Section fissurée")
        printligne("-", "x1", "cm", f"{self.x1_te()*100:.2f}")
        printligne("-", "Icf", "cm4", f"{self.Icf_te():.8f}")
        printligne("-", "Sc", "MPa", f"{self.Sc_te_fissuree():.2f}")
        printligne("-", "Ss1", "MPa", f"{self.Ss1_te_fissuree():.2f}")
        printligne("-", "Ss2", "MPa", f"{self.Ss2_te_fissuree():.2f}")

    def resultat_court(self):
        pass


###############################################################################
# Fonction test
###############################################################################

if __name__ == "__main__":
    situation = "Durable"
    situation = SituationProjet(situation)

    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    beton = BetonArme(
        situation,
        classeexposition,
        classeresistance,
        acc,
        act,
        age,
        classeciment,
        ae,
        fiinft0,
    )

    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)

    Mser = 3.227 / 100
    bw = 18 / 100
    beff = 18 / 100
    h = 60 / 100
    hf = 0 / 100
    c1 = 5 / 100
    c2 = 3 / 100
    As1 = 1.65 / 1e4
    As2 = 0 / 1e4
    vc = VerifContrainteELSSectionRectangulaire(
        beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2
    )
    vc.resultat_long()
