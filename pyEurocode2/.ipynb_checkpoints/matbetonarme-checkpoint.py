from math import *
from pyEurocode2.constante import *

class BetonArme:
    """ret"""
    
    def __init__(self, classeexposition='XC3', classeresistance='C25/30', acc=1, act=1, age=28, classeciment="N", gamma_c = 1.5, fiinft0 = 2.):
        self.classeexposition = classeexposition
        self.classeresistance = classeresistance
        self.acc = acc
        self.act = act
        self.age = age
        self.classeciment = classeciment
        self.gamma_c = gamma_c
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
    
    def fck_cube(self):
        listeCR = ['C12/15', 'C16/20', 'C20/25', 'C25/30', 'C30/37', 'C35/45', 'C40/50',
                   'C45/55', 'C50/60', 'C55/67', 'C60/75', 'C70/85', 'C80/95', 'C90/105']
        fck_cube = [15., 20., 25., 30., 37., 45., 50., 55., 60., 67., 75., 85., 95., 105.]
        CR = listeCR.index(self.classeresistance)
        fck_cube = fck_cube[CR]
        return fck_cube
    
    def fcm(self):
        """Calcul fcm"""
        return self.fck() + 8.
        
    def fctm(self):
        if self.fck() <= 50.:
            return 0.3 * pow(self.fck(), 2./3.)
        else:
            return 2.12 * log10(1. + self.fcm() / 10.)
        
    def fctk_005(self):
        return 0.7 * self.fctm()
    
    def fctk_095(self):
        return 1.3 * self.fctm()
    
    def Ecm(self):
        return 22000. * pow(self.fcm() / 10., 0.3)
    
    def Eceff(self):
        return self.Ecm() / (1 + self.fiinft0)
    
    def alpha_e(self):
        return ES / self.Eceff()
        
    def beta_cc_t(self):
        if self.classeciment == 'R' or self.classeciment == 'r': #ciment de classe R
            s = 0.2
        elif self.classeciment == 'N' or self.classeclasse =='n': #ciment de classe N
            s = 0.25
        elif self.classeciment == 'S' or self.classeciment == 's': #ciment de classe S
            s = 0.38
        return exp(s * (1. - sqrt(28. / self.age)))
    
    def fck_t(self):
        if self.age < 28:
            return self.fcm_t() - 8.
        else:
            return self.fck()
    
    def fcm_t(self):
        if self.age < 28:
            return self.beta_cc_t() * self.fcm()
        else:
            return self.fcm()
    
    def fctm_t(self):
        if self.age < 28:
            alpha = 1.
        else:
            alpha = 2./3.
        return pow(self.beta_cc_t(), alpha) * self.fctm()
    
    def Ecm_t(self):
        return self.Ecm() * pow(self.fcm_t() / self.fcm() ,0.3)
        
        
    def fcd(self):
        """Calcul fcd"""
        return self.acc * self.fck() / self.gamma_c   
    
    def fctd(self):
        return self.act * self.fctk_005() / self.gamma_c
       
    def __repr__(self):
        print(f"Caractéristique béton")
        print("-" * 21)
        print(f"Classe d'exposition : {self.classeexposition}")
        print(f"Classe de résistance : {self.classeresistance}")
        print(f"fck = {self.fck():.0f} MPa")
        print(f"fck_cube = {self.fck_cube():.0f} MPa")
        print(f"fcm = {self.fcm()} MPa")
        print(f"fctm = {self.fctm():.2f} MPa")
        print(f"fctk_095 = {self.fctk_095():.2f} MPa")
        print(f"fctk_005 = {self.fctk_005():.2f} MPa")
        print(f"fiinft0 = {self.fiinft0}")
        print(f"Ecm = {self.Ecm():.0f} MPa")
        print(f"Eceff = {self.Eceff():.0f} MPa")
        print(f"alpha_e = {self.alpha_e()}")
        print("-" * 21)
        
        print(f"age = {self.age} jours")
        print(f"betacc(t) = {self.beta_cc_t():.2f}")
        print(f"fck(t) = {self.fck_t():.2f} MPa")
        print(f"fcm(t) = {self.fcm_t():.2f} MPa")
        print(f"fctm(t) = {self.fctm_t():.2f} MPa")
        print(f"Ecm(t) = {self.Ecm_t():.0f} MPa")
        print("-" * 21)
        
        print(f"acc = {self.acc}")
        print(f"act = {self.act}")
        print(f"gamma_c = {self.gamma_c}")
        print(f"fcd = {self.fcd():.2f} MPa")
        print(f"fctd = {self.fctd():.2f} MPa")
        
                
        return ""