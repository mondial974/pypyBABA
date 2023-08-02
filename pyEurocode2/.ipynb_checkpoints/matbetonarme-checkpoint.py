from math import *
from pyEurocode2.constante import *

class BetonArme:
    """ret"""
    
    def __init__(self, classeexposition='XC3', classeresistance='C25/30', acc=1, act=1, age=28, classeciment="N", gc = 1.5, fiinft0 = 2.):
        self.classeexposition = classeexposition
        self.classeresistance = classeresistance
        self.acc = acc
        self.act = act
        self.age = age
        self.classeciment = classeciment
        self.gc = gc
        self.fiinft0 = fiinft0
        
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
    
    def fctk095(self):
        return 1.3 * self.fctm()
    
    def Ecm(self):
        return 22000. * pow(self.fcm() / 10., 0.3)
    
    def Eceff(self):
        return self.Ecm() / (1 + self.fiinft0)
    
    def ae(self):
        return ES / self.Eceff()
        
    def betacct(self):
        if self.classeciment == 'R' or self.classeciment == 'r': #ciment de classe R
            s = 0.2
        elif self.classeciment == 'N' or self.classeclasse =='n': #ciment de classe N
            s = 0.25
        elif self.classeciment == 'S' or self.classeciment == 's': #ciment de classe S
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
        return self.Ecm() * pow(self.fcmt() / self.fcm() ,0.3)
        
        
    def fcd(self):
        """Calcul fcd"""
        return self.acc * self.fck() / self.gc   
    
    def fctd(self):
        return self.act * self.fctk005() / self.gc
       
    def __repr__(self):
        print(f"Caractéristique béton")
        print("-" * 21)
        print(f"Classe d'exposition : {self.classeexposition}")
        print(f"Classe de résistance : {self.classeresistance}")
        print(f"fck = {self.fck():.0f} MPa")
        print(f"fckcube = {self.fckcube():.0f} MPa")
        print(f"fcm = {self.fcm()} MPa")
        print(f"fctm = {self.fctm():.2f} MPa")
        print(f"fctk095 = {self.fctk095():.2f} MPa")
        print(f"fctk005 = {self.fctk005():.2f} MPa")
        print(f"fiinft0 = {self.fiinft0}")
        print(f"Ecm = {self.Ecm():.0f} MPa")
        print(f"Eceff = {self.Eceff():.0f} MPa")
        print(f"ae = {self.ae()}")
        print("-" * 21)
        
        print(f"age = {self.age} jours")
        print(f"betacc(t) = {self.betacct():.2f}")
        print(f"fck(t) = {self.fckt():.2f} MPa")
        print(f"fcm(t) = {self.fcmt():.2f} MPa")
        print(f"fctm(t) = {self.fctmt():.2f} MPa")
        print(f"Ecm(t) = {self.Ecmt():.0f} MPa")
        print("-" * 21)
        
        print(f"acc = {self.acc}")
        print(f"act = {self.act}")
        print(f"gc = {self.gc}")
        print(f"fcd = {self.fcd():.2f} MPa")
        print(f"fctd = {self.fctd():.2f} MPa")
        
                
        return ""