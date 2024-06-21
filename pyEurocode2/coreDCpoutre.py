from utilsprint import *
from corematbetonarme import *
from corematacierarmature import *
from coresituationprojet import *

class DCPoutreRectangulaire:
    def __init__(self, beton, acier, bw, h, c):
        self.beton = beton
        self.acier = acier
        self.bw = bw
        self.h = h
        self.c = c

    def Ac(self):
        return self.bw * self.h

    def d(self):
        return self.h - self.c
    
    def Asmin(self):
        Asmin1 = self.Asmin1()
        Asmin2 = self.Asmin2()
        Asmin = max([Asmin1, Asmin2])
        return Asmin
    
    def Asmin1(self):
        fctm = self.beton.fctm()
        fyk = self.acier.fyk()
        bw = self.bw
        d = self.d()
        Asmin1 = 0.26 * fctm / fyk * bw * d
        return Asmin1 * 1e4
    
    def Asmin2(self):
        bw = self.bw
        d = self.d()
        Asmin2 = 0.0013 * bw * d
        return Asmin2 * 1e4
    
    def Asmax(self):
        return 0.04 * self.Ac() * 1e4
    
    def resultat_long(self):
        print(f'As_min_1 = {self.Asmin1():.2f} cm2')
        print(f'As_min_2 = {self.Asmin2():.2f} cm2')
        print(f'As_min = {self.Asmin():.2f} cm2')
        print(f'As_max = {self.Asmax():.2f} cm2')

if __name__ == "__main__":
    bw = 100 / 100
    h = 20 / 100   
    c = 5 / 100    
   
    situation = SituationProjet("Durable")
    
    classe_exposition = "XC3"
    classe_resistance = "C25/30"
    alpha_cc = 1
    alpha_ct = 1
    age = 28
    classe_ciment = "N"
    alpha_e = 15
    fi_infini_t0 = 2

    maitrise_fissuration = True
    beton = BetonArme(situation, classe_exposition, classe_resistance, alpha_cc, alpha_ct, age, classe_ciment, alpha_e, fi_infini_t0, h, maitrise_fissuration)
   
    nuance = "S500A"
    diagramme = "palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    poutre = DCPoutreRectangulaire(beton, acier, bw, h, c)
    poutre.resultat_long()