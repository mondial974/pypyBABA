from math import *

from rich.table import Table
from rich.console import Console

from coreconstante import *
from coresituationprojet import *
from utilsprint import *

RHO_BETON_ARME = 2500


class BetonArme:

    def __init__(self, situation, classeexposition='XC3', classeresistance='C25/30', acc=1, act=1, age=28, classeciment='N', ae=0, fiinft0=2):
        self.situation = situation
        self.classeexposition = classeexposition
        self.classeresistance = classeresistance
        self.acc = acc
        self.act = act
        self.gc = self.situation.gc()
        self.age = age
        self.classeciment = classeciment
        self.ae = ae
        self.fiinft0 = fiinft0

    def set_ae(self, valeur):
        self.ae = valeur

    def affiche_classeresistance(self):
        return 'C12/15 C16/20 C20/25 C25/30 C30/37 C35/45 C40/50 C45/55 C50/60 C55/67 C60/75 C70/85 C80/95 C90/105'

    def fck(self):
        listeCR = ['C12/15', 'C16/20', 'C20/25', 'C25/30', 'C30/37', 'C35/45', 'C40/50',
                   'C45/55', 'C50/60', 'C55/67', 'C60/75', 'C70/85', 'C80/95', 'C90/105']
        fck = [12., 16., 20., 25., 30., 35., 40., 45., 50., 55., 60., 70., 80., 90.]
        CR = listeCR.index(self.classeresistance)
        fck = fck[CR]
        return fck

    def fckcube(self):
        listeCR = ['C12/15', 'C16/20', 'C20/25', 'C25/30', 'C30/37', 'C35/45', 'C40/50',
                   'C45/55', 'C50/60', 'C55/67', 'C60/75', 'C70/85', 'C80/95', 'C90/105']
        fckcube = [15., 20., 25., 30., 37., 45., 50., 55., 60., 67., 75., 85., 95., 105.]
        CR = listeCR.index(self.classeresistance)
        fckcube = fckcube[CR]
        return fckcube

    def fcm(self):
        """Calcul fcm"""
        return self.fck() + 8.

    def fctm(self):
        if self.fck() <= 50.:
            return 0.3 * pow(self.fck(), 2./3.)
        else:
            return 2.12 * log10(1. + self.fcm() / 10.)

    def fctk005(self):
        return 0.7 * self.fctm()

    def fctk005t(self):
        return 0.7 * self.fctmt()

    def fctk095(self):
        return 1.3 * self.fctm()

    def Ecm(self):
        return 22000. * pow(self.fcm() / 10., 0.3)

    def Eceff(self):
        return self.Ecm() / (1 + self.fiinft0)

    def alphae(self):
        if self.ae == 0:
            ae = ES / self.Eceff()
            self.set_ae(ae)
            return ae
        else:
            return self.ae

    def betacct(self):
        if self.classeciment == 'R' or self.classeciment == 'r':  # ciment de classe R
            s = 0.2
        elif self.classeciment == 'N' or self.classeciment == 'n':  # ciment de classe N
            s = 0.25
        elif self.classeciment == 'S' or self.classeciment == 's':  # ciment de classe S
            s = 0.38
        return exp(s * (1. - sqrt(28. / self.age)))

    def fckt(self):
        if self.age < 28:
            return self.fcmt() - 8.
        else:
            return self.fck()

    def fcmt(self):
        if self.age < 28:
            return self.betacct() * self.fcm()
        else:
            return self.fcm()

    def fctmt(self):
        if self.age < 28:
            alpha = 1.
        else:
            alpha = 2./3.
        return pow(self.betacct(), alpha) * self.fctm()

    def Ecmt(self):
        return self.Ecm() * pow(self.fcmt() / self.fcm(), 0.3)

    def fcd(self):
        """Calcul fcd"""
        return self.eta() * self.acc * self.fckt() / self.gc

    def fctd(self):
        return self.act * self.fctk005t() / self.gc

    def k1(self):
        dict_k1 = {'X0': 1, 'XC1': 1, 'XC2': 1, 'XC3': 1, 'XC4': 1,
                   'XD1': 0.6, 'XD2': 0.6, 'XD3': 0.6,
                   'XS1': 0.6, 'XS2': 0.6, 'XS3': 0.6,
                   'XF1': 0.6, 'XF2': 0.6, 'XF3': 0.6, 'XF4': 0.6,
                   'XA1': 1, 'XA2': 1, 'XA3': 1}
        return dict_k1[self.classeexposition]

    def Scbar(self):
        return self.k1() * self.fck()

    def lmbda(self):
        if self.fck() <= 50:
            return 0.8
        else:
            return 0.8 - (self.fck() - 50) / 400

    def eta(self):
        if self.fck() <= 50:
            return 1
        else:
            return 1 - (self.fck() - 50) / 100

    def resultatdetail(self):
        w = 40
        tableau = Table(title="PARAMETRE BETON ARME")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="left")
        tableau.add_column("Valeur", justify="right")
        tableau.add_column("unité", justify="left")
        tableau.add_row("Classe d'exposition", "-", f"{self.classeexposition}", "-")
        tableau.add_row("Classe de résistance", "-", f"{self.classeresistance}", "-")
        tableau.add_row("Classe de ciment    ", "-", f"{self.classeciment}", "-")
        tableau.add_row("Résistance caractéritique en compression", "fck", f"{self.fck():.0f}", "MPa")
        tableau.add_row("", "fckcube", f"{self.fckcube():.0f}", "MPa")
        tableau.add_row("", "fcm", f"{self.fcm():.0f}", "MPa")
        tableau.add_row("Résistance caractéristique en traction", "fctm", f"{self.fctm():.2f}", "MPa")
        tableau.add_row("", "fctk095", f"{self.fctk095():.2f}", "MPa")
        tableau.add_row("", "fctk005", f"{self.fctk005():.2f}", "MPa")
        tableau.add_row("Coefficient de fluage", "fiinft0", f"{self.fiinft0}", "-")
        tableau.add_row("Module d'elacticité sécant", "Ecm", f"{self.Ecm():.0f}", "MPa")
        tableau.add_row("Module d'élasticité effectif", "Eceff", f"{self.Eceff():.0f}", "MPa")
        tableau.add_row("Coefficient d'équivalence", "ae", f"{self.alphae():.0f}", "-")
        tableau.add_row("", "", "", "")
        tableau.add_row("Age du béton", "age", f"{self.age}", "jours")
        tableau.add_row("", "betacc(t)", f"{self.betacct():.2f}", "-")
        tableau.add_row("Résistance caractéritique en compression", "fck(t)", f"{self.fckt():.2f}", "MPa")
        tableau.add_row("", "fcm(t)", f"{self.fcmt():.2f}", "MPa")
        tableau.add_row("Résistance caractéristique en traction", "fctm(t)", f"{self.fctmt():.2f}", "MPa")
        tableau.add_row("Module d'elacticité sécant", "Ecm(t)", f"{self.Ecmt():.0f}", "MPa")
        tableau.add_row("", "", "", "")
        tableau.add_row("", "acc", f"{self.acc}", "-")
        tableau.add_row("", "act", f"{self.act}", "-")
        tableau.add_row("", "gc", f"{self.gc}", "-")
        tableau.add_row("Résistance de calcul en compression", "fcd", f"{self.fcd():.2f}", "MPa")
        tableau.add_row("Résistance de calcul en traction", "fctd", f"{self.fctd():.2f}", "MPa")
        console = Console()
        console.print(tableau)

    def __repr__(self):
        printentete()
        printligne("Classe d'exposition", "-", "-", f'{self.classeexposition}')
        printligne("Classe de résistance", "-", "-", f'{self.classeresistance}')
        printligne("Classe de ciment    ", "-", "-", f'{self.classeciment}')
        printligne("Résistance caractéritique en compression", "fck", "MPa", f'{self.fck():.0f}')
        printligne("", "fckcube", "MPa", f'{self.fckcube():.0f}')
        printligne("", "fcm", "MPa", f'{self.fcm():.0f}')
        printligne("Résistance caractéristique en traction", "fctm", "MPa", f'{self.fctm():.2f}')
        printligne("", "fctk095", "MPa", f'{self.fctk095():.2f}')
        printligne("", "fctk005", "MPa", f'{self.fctk005():.2f}')
        printligne("Coefficient de fluage", "fiinft0", "-", f'{self.fiinft0:.2f}')
        printligne("Module d'elacticité sécant", "Ecm", "MPa", f'{self.Ecm():.0f}')
        printligne("Module d'élasticité effectif", "Eceff", "MPa", f'{self.Eceff():.0f}')
        printligne("Coefficient d'équivalence", "ae", "-", f'{self.alphae():.0f}')
        printsep()
        printligne("Age du béton", "age", "jour", f'{self.age:.0f}')
        printligne("", "betacc(t)", "-", f'{self.betacct():.3f}')
        printligne("Résistance caractéritique en compression", "fck(t)", "MPa", f'{self.fckt():.2f}')
        printligne("", "fcm(t)", "MPa", f'{self.fcmt():.2f}')
        printligne("Résistance caractéristique en traction", "fctm(t)", "MPa", f'{self.fctmt():.2f}')
        printligne("Module d'elacticité sécant", "Ecm(t)", "MPa", f'{self.Ecmt():.0f}')
        printsep()
        print("A l'ELU")
        printligne("", "acc", "-", f'{self.acc:.2f}')
        printligne("", "act", "-", f'{self.act:.2f}')
        printligne("", "gc", "-", f'{self.gc:.2f}')
        printligne("", "eta", "-", f'{self.eta():.2f}')
        printligne("", "lambda", "-", f'{self.lmbda():.2f}')
        printligne("Résistance de calcul en compression", "fcd", "MPa", f'{self.fcd():.2f}')
        printligne("Résistance de calcul en traction", "fctd", "MPa", f'{self.fctd():.2f}')
        printsep()
        print("A l'ELS")
        printligne("", "k1", "MPa", f'{self.k1():.2f}')
        printligne("", "Scbar", "MPa", f'{self.Scbar():.2f}')
        printsep()


if __name__ == '__main__':
    situation = SituationProjet('Durable')
    beton = BetonArme(situation, classeexposition='XS1', classeresistance='C30/37', acc=1, act=1, age=7, classeciment="N", ae=0, fiinft0=2)
    # beton.resultatdetail()
    beton.__repr__()