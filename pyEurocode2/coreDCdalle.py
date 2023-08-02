from coreDCpoutre import *
from corematbetonarme import *
from corematacierarmature import *
from coresituationprojet import *

class DC_Dalle():
    
    def __init__(self, beton, acier, h, c, As) :
        self.beton = beton
        self.acier = acier
        self.h = h
        self.c = c
        self.As = As
    
    def Asx_min_dalle(self):
        bw = 100 / 100
        dcpoutre = DCPoutreRectangulaire(self.beton, self.acier, bw, self.h, self.c)
        Asmin_poutre = dcpoutre.Asmin()
        return min(1.2 * self.As, Asmin_poutre)
    
    def smax_slabs_princ(self):
        return min(3 * self.h, 0.40)
    
    def smax_slabs_second(self):
        return min(3.5 * self.h, 0.45)

if __name__ == "__main__":
    situation = "Durable"
    situation = SituationProjet(situation)
    
    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc= 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    
    nuance = "S500B"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    h = 20 / 100
    c = 3 / 100
    As = 1.91 / 1e4
    dcdalle = DC_Dalle(beton, acier, h, c, As)
    print(f"Asmin = {dcdalle.Asmin()*1e4:.2f}")          