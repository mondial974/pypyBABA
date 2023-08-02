#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt
from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *


class PoteauRectCompressionSimple:

    def __init__(self, beton, acier, b, h, c, l, kf, NEd, Asl):
        self.beton = beton
        self.acier = acier
        self.b = b
        self.h = h
        self.c = c
        self.l = l
        self.kf = kf
        self.NEd = NEd
        self.Asl = Asl

    def l0(self):
        return self.kf * self.l

    def a(self):
        return min(self.b, self.h)

    def lbda(self):
        return self.l0() * sqrt(12) / self.a()

    def islbdasup120(self):
        if self.lbda() < 120:
            return True
        else:
            return False

    def alpha(self):
        if self.lbda() <= 60:
            return 0.86 / (1 + (self.lbda() / 62)**2)
        else:
            return (32 / self.lbda())**1.3
        
    def rho(self):
        return self.Asl / (self.b * self.h)
    
    def delta(self):
        return self.c / self.a()

    def kh(self):
        if self.a() < 0.50:
            return (0.75 + 0.5 * self.a()) * (1 - 6 * self.rho() * self.delta())
        else:
            return 1

    def ks(self):
        if self.acier.fyk() > 500 and self.lbda() > 40:
            return 1.6 - 0.6 * self.acier.fyk() / 500
        else:
            return 1

    def NRd(self):
        kh = self.kh()
        ks = self.ks()
        alpha = self.alpha()
        b = self.b
        h = self.h
        fcd = self.beton.fcd()
        Asl = self.Asl
        fyd = self.acier.fyd()
        return kh * ks * alpha * (b * h * fcd + Asl * fyd)

    def Ac(self):
        return self.b * self.h

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
        printligne("Grand coté", "b", "-", f"{self.b*100:.2f}")
        printligne("Petit coté", "h", "-", f"{self.h*100:.2f}")
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
            print(f"    VERIFIE     : NEd = {self.NEd*100:.2f} T <= NRd = {self.NRd()*100:.2f} T")
        else:
            print(f"    NON VERIFIE : NEd = {self.NEd*100:.2f} T  NEd = {self.NRd()*100:.2f} T")
        
        print("")
        print("Armatures longitudinales")
        print(f"                   Asl = {self.Asl*1e4:.2f} cm2")
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
        if self.h >= 0.15:
            print(f"    VERIFIE     : h = {self.h*100:.0f} cm >= 15 cm")
        else:
            print(f"    NON VERIFIE : h = {self.h*100:.0f} cm < 15 cm")
        
        if self.c <= min(0.30 * self.a(), 0.10):
            print(f"    VERIFIE     : d' = {self.c*100:.2f} cm <= min(0.30*h, 10 cm) = {min(0.30*self.a(), 0.10)*100} cm")
        else:
            print(f"    NON VERIFIE : d' = {self.c*100:.2f} cm > min(0.30*h, 10 cm) = {min(0.30*self.a(), 0.10)*100} cm")
        
        if self.lbda() <= 120:
            print(f"    VERIFIE     : lambda = {self.lbda():.2f} <= 120")
        else:
            print(f"    NON VERIFIE : lambda = {self.lbda():.2f} > 120")
        
        if 20 <= self.beton.fck() and self.beton.fck() <= 50:
            print(f"    VERIFIE     : fck = {self.beton.fck()} MPa compris entre 20 et 50 MPa")
        else:
            print(f"    NON VERIFIE : fck = {self.beton.fck()} MPa n'est pas compris entre 20 et 50 MPa")
        
        print("")      
            
        
if __name__ == "__main__":
    situation = SituationProjet('Durable')
    beton = BetonArme(situation, classeexposition="XC3", classeresistance="C25/30", acc=1, act=1, age=28, classeciment="N", ae=15, fiinft0=2)
    acier = AcierArmature(situation, nuance='S500B', diagramme='Palier incliné', diametre=8)
    b = 30 / 100
    h = 20 / 100
    c = 3.5 / 100
    l = 280 / 100
    kf = 0.7
    Asl = 0 / 1e4
    NEd = 65 / 100
    poteau = PoteauRectCompressionSimple(beton, acier, b, h, c, l, kf, NEd, Asl)
    poteau.resultat_court()
