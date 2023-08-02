from math import cos, sin, asin, pi, degrees
from rich.table import Table
from rich.console import Console
from coreconstante import *
from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from appEffortTranchant import *
from utilsprint import *


class Corbeau:
    def __init__(self, beton, acier, FEd, HEd, ac, aH, bw, h, cnom, t, bp) -> None:
        self.beton = beton
        self.acier = acier
        self.FEd = FEd
        self.HEd = HEd
        self.ac = ac
        self.aH = aH
        self.bw = bw
        self.h = h
        self.cnom = cnom
        self.t = t
        self.bp = bp

    ###############################################################################
    # DEFINIFION DES IS
    ###############################################################################
    def isconsolecourte(self):
        ac = self.ac
        z0 = self.z0()
        if ac < z0:
            return True
        else:
            return False

    ###############################################################################
    # GEOMETRIE
    ###############################################################################
    def d(self):
        h = self.h
        cnom = self.cnom
        return h - cnom

    def z0(self):
        d = self.d()
        a = self.a()
        teta = self.teta()
        return d - a / 2 / cos(teta)

    ###############################################################################
    # BIELLE
    ###############################################################################
    def teta_th(self):
        FEd = self.FEd
        HEd = self.HEd
        aH = self.aH
        ac = self.ac
        bw = self.bw
        d = self.d()
        SRdmax = self.SRdmax()
        return 0.5 * asin((FEd + HEd * aH / ac) / (bw * (d - ac) * SRdmax))

    def teta(self):
        teta_th = self.teta_th()
        if teta_th < pi / 4:
            return pi / 4.0
        else:
            return teta_th

    def SRdmax(self):
        fcd = self.beton.fcd()
        return fcd

    def Fc(self):
        FEd = self.FEd
        HEd = self.HEd
        aH = self.aH
        ac = self.ac
        teta = self.teta()
        return (FEd + HEd * aH / ac) / sin(teta)

    ###############################################################################
    # NOEUD
    ###############################################################################
    def a(self):
        Fc = self.Fc()
        bw = self.bw
        SRdmax = self.SRdmax()
        return Fc / (bw * SRdmax)

    def ahh(self):
        a = self.a()
        teta = self.teta_th()
        return a * sin(teta)

    def av(self):
        a = self.a()
        teta = self.teta()
        return a * cos(teta)

    def fc(self):
        Fc = self.Fc()
        bw = self.bw
        a = self.a()
        return Fc / (bw * a)

    def fcv(self):
        Fc = self.Fc()
        teta = self.teta()
        bp = self.bp
        av = self.av()
        return Fc * cos(teta) / (bp * av)

    def fch(self):
        Fc = self.Fc()
        teta = self.teta()
        bp = self.bp
        ahh = self.ahh()
        return Fc * sin(teta) / (bp * ahh)

    ###############################################################################
    # TIRANT
    ###############################################################################
    def Fs(self):
        FEd = self.FEd
        ac = self.ac
        z0 = self.z0()
        HEd = self.HEd
        aH = self.aH
        return FEd * ac / z0 + HEd * (1 + aH / z0)

    ###############################################################################
    # EFFORT TRANCHANT
    ###############################################################################
    def VRdc(self):
        Asw = 0
        s = 0
        beton = self.beton
        acier = self.acier
        redistribution = "Poutre"
        VEdmax = self.FEd
        VEdred = self.FEd
        NEd = 0
        bw = self.bw
        h = self.h
        c1 = self.cnom
        Asl = self.Asmain()
        alpha = 90
        teta = 90
        efforttranchant = EffortTranchant(
            beton,
            acier,
            redistribution,
            VEdmax,
            VEdred,
            NEd,
            bw,
            h,
            c1,
            Asl,
            Asw,
            s,
            alpha,
            teta,
        )
        return efforttranchant.VRdc()

    ###############################################################################
    # ARMATURES
    ###############################################################################

    def Asmain(self):
        Fs = self.Fs()
        fyd = self.acier.fyd()
        return Fs / fyd

    def Ashlnk(self):
        Asmain = self.Asmain()
        return 0.25 * Asmain

    def Asvlnk(self):
        ac = self.ac
        h = self.h
        FEd = self.FEd
        VRdc = self.VRdc()
        fyd = self.acier.fyd()
        if 0.5 * h and FEd > VRdc:
            return 0.5 * FEd / fyd
        else:
            return 0

    ###############################################################################
    # AFFICHAGE DES RESULTATS
    ###############################################################################

    def resultat_long(self):
        printligne(
            "Est-ce une console courte ?", "ac < z0 ?", "", f"{self.isconsolecourte()}"
        )
        print("")
        printentete()
        printligne("Situation de projet", "-", "-", f"{self.beton.situation.situation}")
        print("")
        print("Béton armé")
        printligne(
            "  Résistance caract. en compression",
            "fck",
            "MPa",
            f"{self.beton.fck():.2f}",
        )
        printligne(
            "  Résistance de calcul en compression",
            "fcd",
            "MPa",
            f"{self.beton.fcd():.2f}",
        )
        printligne(
            "  Résistance caract. en traction", "fyk", "MPa", f"{self.acier.fyk():.0f}"
        )
        printligne(
            "  Résistance de calcul en traction",
            "fyd",
            "MPa",
            f"{self.acier.fyd():.0f}",
        )
        print("")
        printsep()
        print("Géométrie")
        printligne("  Epaisseur corbeau", "bw", "cm", f"{self.bw*100:.2f}")
        printligne("  Hauteur corbeau", "h", "cm", f"{self.h*100:.2f}")
        printligne("  Hauteur utile", "d", "cm", f"{self.d()*100:.2f}")
        printligne("  Enrobage corbeau", "cnom", "cm", f"{self.cnom*100:.2f}")
        printligne("  Profondeur appui", "t", "cm", f"{self.t*100:.2f}")
        printligne("  Largeur appui", "bp", "cm", f"{self.bp*100:.2f}")
        print("")
        printsep()
        print("Sollicitations")
        printligne("  Effort vertical", "FEd", "T", f"{self.FEd*100:.2f}")
        printligne("  Distance", "ac", "cm", f"{self.ac*100:.1f}")
        printligne("  Effort horizontal", "HEd", "T", f"{self.HEd*100:.2f}")
        printligne("  Distance", "aH", "cm", f"{self.aH*100:.1f}")
        print("")
        printsep()
        print("Bielle")
        printligne(
            "  Contrainte admissible dans la bielle",
            "SRdmax",
            "MPa",
            f"{self.SRdmax():.2f}",
        )
        printligne(
            "  Inclinaison de la bielle", "teta", "deg", f"{degrees(self.teta()):.2f}"
        )
        printligne("  Bras de levier", "z0", "cm", f"{self.z0()*100:.1f}")
        printligne(
            "  Effort de compression dans la bielle", "Fc", "T", f"{self.Fc()*100:.2f}"
        )
        printligne("  Largeur bielle de compression", "a", "cm", f"{self.a()*100:.2f}")
        printligne("", "ah", "cm", f"{self.ahh()*100:.2f}")
        printligne("", "av", "cm", f"{self.av()*100:.2f}")
        printligne("  Contrainte bielle de compression", "fc", "T", f"{self.fc():.2f}")
        printligne("", "fcv", "MPa", f"{self.fcv():.2f}")
        printligne("", "fch", "MPa", f"{self.fch():.2f}")
        print("")
        printsep()
        print("Tirant")
        printligne(
            "  Effort de traction dans les armatures", "Fs", "T", f"{self.Fs()*100:.2f}"
        )
        printligne(
            "  Armatures horizontales principales",
            "Asmain",
            "cm2",
            f"{self.Asmain()*1e4:.2f}",
        )
        printligne(
            "  Armatures horizontales Secondaires",
            "Ashlnk",
            "cm2",
            f"{self.Ashlnk()*1e4:.2f}",
        )
        print("")
        printsep()
        print("Tranchant")
        printligne("  Effort résistant", "VRdc", "T", f"{self.VRdc()*100:.2f}")
        printligne(
            "  Armatures verticales", "Asvlnk", "cm2", f"{self.Asvlnk()*1e4:.2f}"
        )
        printsep()


###############################################################################
# TEST
###############################################################################
if __name__ == "__main__":
    situation = SituationProjet("Durable")
    beton = BetonArme(
        situation,
        classeexposition="XC3",
        classeresistance="C25/30",
        classeciment="N",
        acc=1,
        act=1,
        age=28,
        ae=15,
        fiinft0=2,
    )
    acier = AcierArmature(
        situation, nuance="S500B", diagramme="Palier incliné", diametre=8
    )
    corbeau = Corbeau(
        beton,
        acier,
        FEd=18.9 / 100,
        HEd=3.6 / 100,
        ac=25 / 100,
        aH=2 / 100,
        bw=40 / 100,
        h=35 / 100,
        cnom=3.5 / 100,
        t=50 / 100,
        bp=40 / 100,
    )
    corbeau.resultat_long()
