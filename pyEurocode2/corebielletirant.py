from corematbetonarme import *


class Bielle:
      
    def __init__(self, type, beton, F=0, a=0, bw=0, k1=1, k2=0.85, k3=0.75):
        self.type = type
        self.F = F
        self.a = a
        self.bw = bw
        self.beton = beton
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        
    def SRdmax(self):
        upsilonprime = 1 - self.beton.fck() / 250
        listeSRdmax = [self.beton.fcd(),
                  0.6 * upsilonprime * self.beton.fcd(),
                  self.k1 * upsilonprime * self.beton.fcd(),
                  self.k2 * upsilonprime * self.beton.fcd(),
                  self.k3 * upsilonprime * self.beton.fcd()]
        SRdmax = listeSRdmax[self.type-1]
        return SRdmax
    
    def SEd(self):
        return self.F / (self.a * self.bw)     
    
    def verifcontrainte(self):
        if self.SEd() <= self.SRdmax():
            print(f"SEd = {self.SEd():.2f} < SRdmax = {self.SRdmax():.2f} => VERIFIE")
        else:
            print(f"SEd = {self.SEd():.2f} > SRdmax = {self.SRdmax():.2f} => !!! NON VERIFIE")


class Noeud:
    
    def __init__(self, type, beton, FEcd0=0, FEcd1=0, FEcd2=0, FEcd3=0, teta2=45, teta3=45, lbd=0.01,
                 a0=0.01, a1=0.01, a2=0.01, a3=0.01, bw=0.01, k1=1, k2=0.85, k3=0.75):
        self.type = type
        self.beton = beton
        self.FEcd0 = FEcd0
        self.FEcd1 = FEcd1
        self.FEcd2 = FEcd2
        self.FEcd3 = FEcd3
        self.teta2 = radians(teta2)
        self.teta3 = radians(teta3)
        self.lbd = lbd
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.bw = bw
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
    
    def SRdmax(self):
        upsilonprime = 1 - self.beton.fck() / 250
        listeSRdmax = [self.k1 * upsilonprime * self.beton.fcd(),
                       self.k2 * upsilonprime * self.beton.fcd(),
                       self.k3 * upsilonprime * self.beton.fcd()]
        SRdmax = listeSRdmax[self.type-1]
        return SRdmax
    
    def SEd0(self):
        return self.FEcd0 / (self.a0 * self.bw) 
    
    def SEd1(self):
        return self.FEcd1 / (self.a1 * self.bw) 
    
    def SEd2(self):
        return self.FEcd2 / (self.a2 * self.bw) 
    
    def SEd3(self):
        return self.FEcd3 / (self.a3 * self.bw) 
    
    def verifSEd0(self):
        if self.SEd0() <= self.SRdmax():
            print(f"SEd0 = {self.SEd0():.2f} < SRdmax = {self.SRdmax():.2f} => VERIFIE")
        else:
            print(f"SEd0 = {self.SEd0():.2f} > SRdmax = {self.SRdmax():.2f} => !!! NON VERIFIE")
    
    def verifSEd1(self):
        if self.SEd1() <= self.SRdmax():
            print(f"SEd1 = {self.SEd1():.2f} < SRdmax = {self.SRdmax():.2f} => VERIFIE")
        else:
            print(f"SEd1 = {self.SEd1():.2f} > SRdmax = {self.SRdmax():.2f} => !!! NON VERIFIE")
    
    def verifSEd2(self):
        if self.SEd2() <= self.SRdmax():
            print(f"SEd2 = {self.SEd2():.2f} < SRdmax = {self.SRdmax():.2f} => VERIFIE")
        else:
            print(f"SEd2 = {self.SEd2():.2f} > SRdmax = {self.SRdmax():.2f} => !!! NON VERIFIE")
    
    def verifSEd3(self):
        if self.SEd3() <= self.SRdmax():
            print(f"SEd3 = {self.SEd3():.2f} < SRdmax = {self.SRdmax():.2f} => VERIFIE")
        else:
            print(f"SEd3 = {self.SEd3():.2f} > SRdmax = {self.SRdmax():.2f} => !!! NON VERIFIE")    