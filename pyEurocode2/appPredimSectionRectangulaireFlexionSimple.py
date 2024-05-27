from math import *
from numpy import cbrt
from coresituationprojet import *
from corematbetonarme import *
from utilsprint import *


class PredimSectionRectangulaireFlexionSimple:

    def __init__(self, situation, beton, Mu, mu_lu, k) -> None:
        self.situation = situation
        self.beton = beton
        self.Mu = Mu
        self.mu_lu = mu_lu
        self.k = k

    def d(self):
        Mu = self.Mu
        mu_lu = self.mu_lu
        k = self.k
        fcd = self.beton.fcd()
        return round(cbrt(Mu / (k * mu_lu * fcd)), 2)

    def bw(self):
        k = self.k
        d = self.d()
        return round(k * d, 2)

    def hArrondi(self):
        h = trunc(self.d()*100+5)
        while (h) % 5 != 0:
            h += 1
        return h / 100

    def bwArrondi(self):
        bw = trunc(self.bw()*100)
        while (bw) % 5 != 0:
            bw += 1
        return bw / 100

    def resultat_long(self):
        printentete()
        print("Donnée d'entrée")
        printligne("Moment ELU", "Mu", "T.m", f"{self.Mu*100:.2f}")
        printligne("Moment limite ultime", "mu_lu", "-", f"{self.mu_lu:.4f}")
        printligne("Ratio bw / d", "k", "-", f"{self.k:.2f}")
        printsep()
        print("Résultat")
        printligne("Largeur poutre", "bw", "cm", f"{self.bwArrondi()*100:.2f}")
        printligne("Hauteur utile poutre", "d", "cm", f"{self.hArrondi()*100:.2f}")
        printfintab()

    def resultat_court(self):
        print(f"Poutre {self.bwArrondi()*100:.0f} x {self.hArrondi()*100:.0f} ht")


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

    Mu = 32 / 100
    mu_lu = 0.2252
    k = 0.5
    predim = PredimSectionRectangulaireFlexionSimple(situation, beton, Mu, mu_lu, k)
    predim.resultat_court()