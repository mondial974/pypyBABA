from corematbetonarme import *
from corematacierarmature import *


class LongueurRecouvrementBarre:
    
    def __init__(self, beton, acier, conditionBetonnage, sollicitation, asReq, asProv, a1, a2, a3, a4, a5, a6):
        self.beton = beton
        self.acier = acier
        self.conditionBetonnage = conditionBetonnage
        self.sollicitation = sollicitation
        self.asReq = asReq
        self.asProv = asProv
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a5
        self.a6 = a6
        
    def eta1(self):
        if self.conditionBetonnage == "Bonne":
            return 1
        else:
            return 0.7
        
    def eta2(self):
        diamBarre = self.acier.diametre * 1000
        if diamBarre <= 32:
            return 1
        else:
            return (132 - diamBarre) / 100
    
    def fctd(self):
        return self.beton.fctd()
        
    def fbd(self):
        eta1 = self.eta1()
        eta2 = self.eta2()
        fctd = self.fctd()
        return 2.25 * eta1 * eta2 * fctd
    
    def fyk(self):
        return self.acier.fyk()
    
    def sigmaSd(self):
        asReq = self.asReq
        asProv = self.asProv
        fyk = self.fyk()        
        return asReq / asProv * fyk
        
    def lb(self):
        diamBarre = self.acier.diametre
        fyk = self.fyk()
        fbd = self.fbd()
        return diamBarre / 4 * fyk / fbd
    
    def lbrqd(self):
        diamBarre = self.acier.diametre
        sigmaSd = self.sigmaSd()
        fbd = self.fbd()
        return diamBarre / 4 * sigmaSd / fbd
    
    def lbmin(self):
        sollicitation = self.sollicitation
        lbrqd = self.lbrqd()
        diamBarre = self.acier.diametre 
        
        if sollicitation == "Traction":
            return max(0.3 * lbrqd, 10 * diamBarre, 100/1000)
        else:
            return max(0.6 * lbrqd, 10 * diamBarre, 100/1000)
        
    def lbd(self):
        a1 = self.a1
        a2 = self.a2
        a3 = self.a3
        a4 = self.a4
        a5 = self.a5
        lbrqd = self.lbrqd()
        lbmin = self.lbmin()
        
        return max(max(a1 * a2 * a3 * a4 * a5 * lbrqd,
                0.7 * a1 * a4 * lbrqd),
                   lbmin)
    
    def l0min(self):
        lbrqd = self.lbrqd()
        a6 = self.a6
        diamBarre = self.acier.diametre 
        return max(0.3 * a6 * lbrqd, 15 * diamBarre, 200/1000)
                
    def l0(self):
        a1 = self.a1
        a2 = self.a2
        a3 = self.a3
        a4 = self.a4
        a5 = self.a5
        a6 = self.a6
        lbrqd = self.lbrqd()
        l0min = self.l0min()
        
        return max(a1 * a2 * a3 * a4 * a5 * a6 * lbrqd,
                   0.7 * a1 * a4 * lbrqd,
                   l0min)
        
        
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
    
    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 20
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    conditionBetonnage = "Bonne"
    sollicitation = "Traction"
    a1 = 1
    a2 = 0.85
    a3 = 0.95
    a4 = 1
    a5 = 1
    a6 = 1
    asReq = 0.884 / 1e4
    asProv = 1 / 1e4
    lrb = LongueurRecouvrementBarre(beton, acier, conditionBetonnage, sollicitation, asReq, asProv, a1, a2, a3, a4, a5, a6)
    
    print(f"eta1 = {lrb.eta1()}")
    print(f"eta2 = {lrb.eta2()}")
    print(f"fctd = {lrb.fctd()}")
    print(f"fbd = {lrb.fbd()}")
    print(f"lbrqd = {lrb.lbrqd()*100}")
    print(f"Ss = {lrb.sigmaSd()}")
    print(f"lbmin = {lrb.lbmin()*100}")
    print(f"lbd = {lrb.lbd()*100}")
    
    print(f"l0 = {lrb.l0()*100}")
    