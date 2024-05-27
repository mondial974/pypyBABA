
from colorama import Fore, Style
from rich.table import Table
from rich.console import Console
from utilsmath import *
from math import atan, degrees
from corematbetonarme import *
from corematacierarmature import *


class CroisementPoutre():

    def __init__(self, beton, acier, bw1, h1, ai1, bw2, c2, ai2, dsup, dh1, VEd) -> None:
        self.beton = beton
        self.acier = acier
        self.bw1 = bw1
        self.h1 = h1
        self.ai1 = ai1
        self.bw2 = bw2
        self.c2 = c2
        self.ai2 = ai2
        self.dsup = dsup
        self.dh1 = dh1
        self.VEd = VEd

    def dinf(self):
        ai1 = self.ai1
        ai2 = self.ai2
        return ai2 - ai1

    def h2(self):
        h1 = self.h1
        dinf = self.dinf()
        return h1 - dinf

    def hc2(self):
        h2 = self.h2()
        dsup = self.dsup
        return h2 - dsup

    def dc2(self):
        hc2 = self.hc2()
        c2 = self.c2
        return hc2 - c2

    def zc2(self):
        dc2 = self.dc2()
        return 0.9 * dc2

    def lbd2(self):
        bw1 = self.bw1
        dh1 = self.dh1
        return bw1 - dh1

    def teta1(self):
        hc2 = self.hc2()
        c2 = self.c2
        bw1 = self.bw1
        dh1 = self.dh1
        c2 = self.c2
        return atan((hc2 - 2 * c2) / (bw1 - dh1 + c2))

    def vEd(self):
        VEd = self.VEd
        bw2 = self.bw2
        zc2 = self.zc2()
        return VEd / (bw2 * zc2)

    def VRdmax(self):
        fck = self.beton.fck()
        fcd = self.beton.fcd()
        bw2 = self.bw2
        zc2 = self.zc2()
        teta1 = self.teta1()
        v1 = 0.6 * (1 - fck / 250)
        return bw2 * zc2 * v1 * fcd * cot(teta1) / (1 + cot2(teta1))

    def vRdmax(self):
        bw2 = self.bw2
        zc2 = self.zc2()
        VRdmax = self.VRdmax()
        return VRdmax / (bw2 * zc2)

    def section_As(self):
        VEd = self.VEd
        fyd = self.acier.fyd()
        return VEd / fyd

    def pr(a, b, c, d):
        print(f"{a:10} | {b:5} = {c:5}  {d:10}")

    def resultatdetail(self):
        def prOK(texte):
            print(Fore.LIGHTGREEN_EX + texte + Style.RESET_ALL)

        def prERROR(texte):
            print(Fore.RED + texte + Style.RESET_ALL)

        w = 45

        print(f"dinf + dsup = {(self.dinf() + self.dsup)*100:.0f}")

        tableau = Table(title="PARAMETRE BETON ARME")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="left")
        tableau.add_column("Valeur", justify="center")
        tableau.add_column("unité", justify="right")
        tableau.add_row("Résistance caractéristique béton", "fck", f"{self.beton.fck():.0f}", "MPa")
        tableau.add_row("Résistance de calcul béton", "fcd", f"{self.beton.fcd():.2f}", "MPa")
        tableau.add_row("Résistance caractéristique acier", "fyk", f"{self.acier.fyk():.0f}", "MPa")
        tableau.add_row("Résistance de calcul acier", "fyd", f"{self.acier.fyd():.2f}", "MPa")
        console = Console()
        console.print(tableau)

        tableau = Table(title="PARAMETRE POUTRE 1")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="center")
        tableau.add_column("Valeur", justify="center")
        tableau.add_column("unité", justify="right")
        tableau.add_row("Largeur poutre 1", "bw1", f"{self.bw1*100:.0f}", "cm")
        tableau.add_row("Hauteur poutre 1", "h1", f"{self.h1*100:.0f}", "cm")
        console = Console()
        console.print(tableau)

        tableau = Table(title="PARAMETRE POUTRE 2")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="center")
        tableau.add_column("Valeur", justify="center")
        tableau.add_column("unité", justify="right")
        tableau.add_row("Largeur poutre 2", "bw2", f"{self.bw2*100:.1f}", "cm")
        tableau.add_row("Hauteur poutre 2", "h2", f"{self.h2()*100:.1f}", "cm")
        tableau.add_row("Enrobage général poutre 2", "c2", f"{self.c2*100:.1f}", "cm")
        tableau.add_row("Hauteur utile cisailleemnt poutre 2", "dc2", f"{self.dc2()*100:.1f}", "cm")
        tableau.add_row("Décalage inférieur de la poutre 2", "dinf", f"{self.dinf()*100:.1f}", "cm")
        tableau.add_row("Hauteur de cisaillement de la poutre 2", "hc2", f"{self.hc2()*100:.1f}", "cm")
        tableau.add_row("Bras de levier ", "zc2", f"{self.zc2()*100:.1f}", "cm")
        tableau.add_row("Longueur d'ancragede la poutre 2", "lbd2", f"{self.lbd2()*100:.1f}", "cm")
        tableau.add_row("Inclinaison de la bielle d'appui", "teta1", f"{degrees(self.teta1()):.2f}", "°")
        console = Console()
        console.print(tableau)

        tableau = Table(title="VERIFICATION CISAILLEMENT SUR APPUIS POUTRE 2")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="center")
        tableau.add_column("Valeur", justify="center")
        tableau.add_column("unité", justify="right")
        tableau.add_row("Contrainte de cisaillement", "vEd", f"{self.vEd():.2f}", "MPa")
        tableau.add_row("Contrainte de cisaillement limite", "vRdmax", f"{self.vRdmax():.2f}", "MPa")
        console = Console()
        console.print(tableau)
        if self.vEd() <= self.vRdmax():
            prOK("vEd <= vRdmax ==> VERIFIE")
        else:
            prERROR("vEd > vRdmax ==> NON VERIFIE")

        print("")
        tableau = Table(title="ARMATURES")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="center")
        tableau.add_column("Valeur", justify="center")
        tableau.add_column("unité", justify="right")
        tableau.add_row("Ancrage et suspente", "As", f"{self.section_As()*1e4:.2f}", "cm2")
        console = Console()
        console.print(tableau)

    def resultatsimpl(self):
        def prOK(texte):
            print(Fore.LIGHTGREEN_EX + texte + Style.RESET_ALL)

        def prERROR(texte):
            print(Fore.RED + texte + Style.RESET_ALL)

        w = 40

        tableau = Table(title="RESULTATS SIMPLIFIES")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="center")
        tableau.add_column("Valeur", justify="center")
        tableau.add_column("unité", justify="right")
        tableau.add_row("Contrainte de cisaillement", "vEd", f"{self.vEd():.2f}", "MPa")
        tableau.add_row("Contrainte de cisaillement limite", "vRdmax", f"{self.vRdmax():.2f}", "MPa")
        tableau.add_row("Ancrage et suspente", "As", f"{self.section_As()*1e4:.2f}", "cm2")
        console = Console()
        console.print(tableau)
        if self.vEd() <= self.vRdmax():
            prOK("vEd <= vRdmax ==> VERIFIE")
        else:
            prERROR("vEd > vRdmax ==> NON VERIFIE")


if __name__ == "__main__":
    situation = "Durable"
    situation = SituationProjet(situation)

    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    alpha_e = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, alpha_e, fiinft0)

    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)

    # Effort tranchant
    VEd = 53 / 100
    # Poutre principale
    bw1 = 60 / 100
    h1 = 100 / 100
    ai1 = 3150 / 100
    dsup = 30 / 100
    # Poutre secondaire
    bw2 = 60 / 100
    h2 = 60 / 100
    c2 = 5 / 100
    ai2 = 3156 / 100
    dh1 = 5 / 100

    croisement = CroisementPoutre(beton, acier, bw1, h1, ai1, bw2, c2, ai2, dsup, dh1, VEd)
    croisement.resultatdetail()