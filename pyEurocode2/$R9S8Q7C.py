import numpy as np

from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from utilsmath import interpolation

ABAQUE = np.array([
       [0.50, 0.0965, 0.2584, 0.167],
       [0.55, 0.0892, 0.2889, 0.1082],
       [0.60, 0.0820, 0.3289, 0.0998],
       [0.65, 0.0750, 0.3781, 0.0916],
       [0.70, 0.0683, 0.4388, 0.0838],
       [0.75, 0.0620, 0.5124, 0.0764],
       [0.80, 0.0561, 0.5964, 0.0694],
       [0.85, 0.0506, 0.6871, 0.0630],
       [0.90, 0.0456, 0.7845, 0.0571],
       [0.95, 0.0410, 0.8887, 0.0517],
       [1.00, 0.0368, 1.00, 0.0468]
       ])

class Dalle4AppuisArticules:
        
    def __init__(self, situation, beton, acier, pu, lx, ly, h, c):
        self.situation = situation
        self.beton = beton
        self.acier = acier
        self.pu = pu
        self.lx = lx
        self.ly = ly
        self.h = h
        self.c = c
    
    def a(self):
        return self.lx / self.ly
    
    def nux(self):
                
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                # Cherche nux
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][1]
                yb = ABAQUE[j+1][1]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
        
        if self.a() == 0.50:
            return ABAQUE[0][1]
        
        if self.a() == 1:
            return ABAQUE[10][1]
    
    def nuy(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][2]
                yb = ABAQUE[j+1][2]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
                
        if self.a() == 0.50:
            return ABAQUE[0][2]
        
        if self.a() == 1:
            return ABAQUE[10][2]
    
    def nuf(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][3]
                yb = ABAQUE[j+1][3]
                x = a
                return interpolation(xa, xb, ya, yb, x)
                
        if self.a() == 0.50:
            return ABAQUE[0][3]
        
        if self.a() == 1:
            return ABAQUE[10][3]
    
    def mx(self):
        return self.nux() * self.pu * self.lx**2
    
    def my(self):
        return self.nuy() * self.mx()
    
    def f(self):
        return self.nuf() * self.p * self.lx**4 / self.h
    
    def resultat_long(self):
        printentete()

if __name__ == "__main__":
    situation = "Durable"
    situation = SituationProjet(situation)
        
    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    gamma_c = situation.gamma_c()
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    
    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    pu = 1.10 / 100
    lx= 300 / 100
    ly = 500 / 100
    ep = 20 / 100
    c = 3 / 100
    dalle = Dalle4AppuisArticules(situation, beton, acier, pu, lx, ly, ep, c)
    dalle.resultat_long()