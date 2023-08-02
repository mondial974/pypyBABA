#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt, pi
from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *


class PoteauCircCompressionSimple:

    def __init__(self, beton, acier, d, c, l, kf, NEd, Asl, repereElement):
        self.beton = beton
        self.acier = acier
        self.d = d
        self.c = c
        self.l = l
        self.kf = kf
        self.NEd = NEd
        self.Asl = Asl
        self.repereElement = repereElement
    
    def l0(self):
        return self.kf * self.l

    def lbda(self):
        return 4 * self.l0() / self.d

    def islbdainf120(self):
        if self.lbda() < 120:
            return True
        else:
            return False

    def alpha(self):
        if self.lbda() <= 60:
            return 0.84 / (1 + (self.lbda() / 52)**2)
        else:
            return (27 / self.lbda())**1.24
        
    def rho(self):
        return self.Asl / self.Ac()
    
    def delta(self):
        return self.c / self.d

    def kh(self):
        if self.d < 0.60:
            return (0.7 + 0.5 * self.d) * (1 - 8 * self.rho() * self.delta())
        else:
            return 1

    def ks(self):
        if self.acier.fyk() > 500 and self.lbda() > 30:
            return 1.6 - 0.65 * self.acier.fyk() / 500
        else:
            return 1

    def NRd(self):
        kh = self.kh()
        ks = self.ks()
        alpha = self.alpha()
        Ac = self.Ac()
        fcd = self.beton.fcd()
        Asl = self.Asl
        fyd = self.acier.fyd()
        return kh * ks * alpha * (Ac * fcd + Asl * fyd)

    def Ac(self):
        return pi * self.d**2 / 4

    def Asmin(self):
        return max(0.1 * self.NEd / self.acier.fyd(), 0.002 * self.Ac())

    def Asmax(self):
        return 0.04 * self.Ac()

    def chercheAsl(self):
        if self.Asl == 0:
            self.Asl = self.Asmin()
            NRd = self.NRd()
            while NRd < self.NEd:
                self.Asl = self.Asl + 0.01 / 1e4
                NRd = self.NRd()
            return self.Asl
        else:
            return self.Asl

    def resultat_long(self):
        self.resultat_court()          
        printentete()
        printligne("Situation de projet", "-", "-", f"{self.beton.situation.situation}")
        print("")
        printsep()
        print("Béton")
        printligne("Résistance du béton en compression", "fck", "-", f"{self.beton.fck():.2f}")
        printligne("Résistance de calcul", "fcd", "-", f"{self.beton.fcd():.2f}")
        print("")
        printsep()
        print("Acier pour armatures")
        printligne("Limite d'élasticité", "fyk", "-", f"{self.acier.fyk():.2f}")
        printligne("Résistance de calcul", "fyd", "-", f"{self.acier.fyd():.2f}")
        print("")
        printsep()
        print("Géométrie")
        printligne("Diamètre", "d", "-", f"{self.d*100:.2f}")
        printligne("Enrobage", "c", "-", f"{self.c*100:.2f}")
        printligne("Section de béton", "Ac", "-", f"{self.Ac()*1e4:.2f}")
        printligne("Longeur poteau", "l", "-", f"{self.l*100:.0f}")
        printligne("Coefficient de flambement", "kf", "-", f"{self.kf:.2f}")
        printligne("Longueur de flambement", "l0", "-", f"{self.l0()*100:.0f}")
        print("")
        printsep()
        print("Efforts")
        printligne("Effort normal sollicitant ELU", "NEd", "-", f"{self.NEd*100:.2f}")
        printligne("Effort résistant", "NRd", "-", f"{self.NRd()*100:.2f}")
        print("")
        printsep()
        print("Paramètres de calcul")
        printligne("Elancement", "lambda", "-", f"{self.lbda():.2f}")
        printligne("Coefficient de calcul", "alpha", "-", f"{self.alpha():.2f}")
        printligne("-", "rho", "-", f"{self.rho():.2f}")
        printligne("-", "delta", "-", f"{self.delta():.2f}")
        printligne("-", "kh", "-", f"{self.kh():.2f}")
        printligne("-", "ks", "-", f"{self.ks():.2f}")
        printsep()
        print("Armatures longitudinales")
        printligne("Section minimale d'armatures", "Asmin", "-", f"{self.Asmin()*1e4:.2f}") 
        printligne("Section d'acier longitudinale", "Asl", "-", f"{self.Asl*1e4:.2f}")
        printligne("Section maximale d'armatures", "Asmax", "-", f"{self.Asmax()*1e4:.2f}") 
        printfintab()        
        
    def resultat_court(self):
        self.chercheAsl()
        printverification()
        print("Effort résistant :") 
        if self.NEd < self.NRd():
            print(f"    VERIFIE     : NRd = {self.NEd*100:.2f} T <= NRd = {self.NRd()*100:.2f} T")
        else:
            print(f"    NON VERIFIE : NRd = {self.NEd*100:.2f} T  NEd = {self.NRd()*100:.2f} T")
        
        print("")
        print("Armatures longitudinales")
        print(f"                  Asl = {self.Asl*1e4:.2f} cm2")
        if self.Asl < self.Asmin():
            print(f"    NON VERIFIE : Asl < Asmin = {self.Asmin()*1e4:.2f} cm2")
        if self.Asl == self.Asmin():
            print(f"    VERIFIE     : Asl = Asmin = {self.Asmin()*1e4:.2f} cm2")            
        if self.Asmin() < self.Asl and self.Asl <= self.Asmax():
            print(f"    VERIFIE     :  Asmin = {self.Asmin()*1e4:.2f} cm2 <= Asl <= Asmax = {self.Asmax()*1e4:.2f} cm2")
        if self.Asl > self.Asmax():
            print(f"    NON VERIFIE : Asl > Asmax = {self.Asmax()*1e4:.2f} cm2")
        
        print("")    
        print("Champ d'application de la méthode")
        if self.d >= 0.15:
            print(f"    VERIFIE     : d = {self.d*100:.0f} cm >= 15 cm")
        else:
            print(f"    NON VERIFIE : d = {self.d*100:.0f} cm < 15 cm")
        
        if self.c <= min(0.30 * self.d, 0.10):
            print(f"    VERIFIE     : d' = {self.c*100:.2f} cm <= min(0.30*h, 10 cm) = {min(0.30*self.d, 0.10)*100} cm")
        else:
            print(f"    NON VERIFIE : d' = {self.c*100:.2f} cm > min(0.30*h, 10 cm) = {min(0.30*self.d, 0.10)*100} cm")
        
        if self.lbda() <= 120:
            print(f"    VERIFIE     : lambda = {self.lbda():.2f} <= 120")
        else:
            print(f"    NON VERIFIE : lambda = {self.lbda():.2f} > 120")
        
        if 20 <= self.beton.fck() and self.beton.fck() <= 50:
            print(f"    VERIFIE     : fck = {self.beton.fck()} MPa compris entre 20 et 50 MPa")
        else:
            print(f"    NON VERIFIE : fck = {self.beton.fck()} MPa n'est pas compris entre 20 et 50 MPa")
        
        print("")   
    
    def minute(self):
        self.chercheAsl()
        print(f"## {self.repereElement}")
        print("") 
        print("### Données d'entrée")
        print(f"- Situation {self.beton.situation.situation}")
        print(f"- Béton {self.beton.classeresistance}")
        print(f"- Acier {self.acier.nuance}")
        print(f"- Diamètre = {self.d*100:.2f} cm")
        print(f"- Enrobage c = {self.c*100:.2f} cm")
        print(f"- Longeur = {self.l*100:.2f} cm")
        print(f"- Coefficient de flambement = {self.kf}")
        print(f"- Effort normal sollicitant = {self.NEd*100:.2f} T")
        print(f"- Armatures longitudinales = {self.Asl*1e4:.2f} cm2")
        print("")
        print(f"### Résultats")
        print(f"- Asl = {self.Asl*1e4:.2f} cm2")      
        print("___")
                
        
if __name__ == "__main__":
    situation = SituationProjet('Durable')
    beton = BetonArme(situation, classeexposition="XC3", classeresistance="C25/30", acc=1, act=1, age=28, classeciment="N", ae=15, fiinft0=2)
    acier = AcierArmature(situation, nuance='S500B', diagramme='Palier incliné', diametre=8)
    d = 40
    c = 3
    l = 318
    kf = 0.7
    Asl = 0
    NEd = 220
    repereElement = "P1"
    poteau = PoteauCircCompressionSimple(beton, acier, d/100, c/100, l/100, kf, NEd/100, Asl/1e4, repereElement)
    poteau.minute()
