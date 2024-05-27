from appLongueurRecouvrementBarre import *
from corematbetonarme import *
from corematacierarmature import *

class PoteauDC:
    
    def __init__(self, beton, acier, b, h, hsd, diamBarreLongMin, diamBarreLongMax, diamBarreTrans, nbBarreTrans, asReq, asProv):
        self.beton = beton
        self.acier = acier
        self.b = b
        self.h = h # petit cote
        self.hsd = hsd # hauteur sous dalle
        self.diamBarreLongMin = diamBarreLongMin
        self.diamBarreLongMax = diamBarreLongMax
        self.diamBarreTrans = diamBarreTrans
        self.nbBarreTrans = nbBarreTrans
        self.asReq = asReq
        self.asProv = asProv
    
    def scltmax(self):
        b = self.b
        diamBarreLongMin = self.diamBarreLongMin / 1000
        return min(20 * diamBarreLongMin, b, 400/1000)
    
    def sclt(self):
        scltmax = self.scltmax()
        return 0.6 * scltmax
    
    def fiLongMini(self):
        return 8
    
    def fiTransMini(self):
        diamBarreLongMax = self.diamBarreLongMax
        return max(6, diamBarreLongMax/4)
    
    def l0(self):
        beton = self.beton
        self.acier.diametre = self.diamBarreLongMax / 1000
        acier = self.acier
        a1 = 1
        a2 = 1
        a3 = 1
        a4 = 0.7
        a5 = 1
        a6 = 1.5
        conditionBetonnage = "Bonne"
        sollicitation = "Compression"
        asReq = self.asReq
        asProv = self.asProv
        lrb = LongueurRecouvrementBarre(beton, acier, conditionBetonnage, sollicitation, asReq, asProv, a1, a2, a3, a4, a5, a6)   
        return lrb.l0()
    
    def lbrqd(self):
        beton = self.beton
        self.acier.diametre = self.diamBarreLongMax / 1000
        acier = self.acier
        a1 = 1
        a2 = 1
        a3 = 1
        a4 = 0.7
        a5 = 1
        a6 = 1.5
        conditionBetonnage = "Bonne"
        sollicitation = "Compression"
        asReq = self.asReq
        asProv = self.asProv
        lrb = LongueurRecouvrementBarre(beton, acier, conditionBetonnage, sollicitation, asReq, asProv, a1, a2, a3, a4, a5, a6)
        return lrb.lbrqd()
    
    def n11e11(self):
        # Zone de recouvrement
        # HA8 >= diamBarreLongMax >= HA14
        h = self.h
        sclt = self.sclt()
        diamBarreLongMax = self.diamBarreLongMax
        
        if (diamBarreLongMax >= 8) or (diamBarreLongMax <=14):
            n11 = 1
            e11 = sclt
            lRep = 3/100 + e11
            while lRep < h:
                lRep = lRep + e11
                n11 = n11 + 1
        
        return [n11, e11*100, lRep*100]
    
    def n12e12(self):
        # diamBarreLongMax > HA14
        l0 = self.l0()
        sclt = self.sclt()
        diamBarreLongMax = self.diamBarreLongMax
        
        if diamBarreLongMax > 14:
            n12 = 1
            e12 = sclt
            lRep = 3/100 + e12
            while lRep < l0:
                lRep = lRep + e12
                n12 = n12 + 1
                
        return [n12, e12*100, lRep*100]
    
    def n131e131(self):
        # diamBarreLongMax > HA20
        l0 = self.l0()
        sclt = self.sclt()
        asReq = self.asReq
        diamBarreLongMax = self.diamBarreLongMax / 1000
        diamBarreTrans = self.diamBarreTrans / 1000
        nbBarreTrans = self.nbBarreTrans
        self.acier.diametre = diamBarreTrans
        acier = self.acier
        asTrans = nbBarreTrans * self.acier.aire_barre()
        e131min = min(sclt, 150/1000) 
        
        l131 = l0 / 3 + 4 * diamBarreLongMax - 3 / 100       
        n131 = 1
        e131 = l131 / n131
        nb131 = 2
        ast = asTrans * nb131
        
        while (ast < asReq / 2) or (e131 > e131min):
            n131 = n131 + 1
            nb131 = nb131 + 1
            e131 = l131 / n131
            ast = ast + asTrans
        
        return [n131, e131*100, (l0/3+4*diamBarreLongMax)*100]
        
    def n132e132(self):
        l0 = self.l0()
        sclt = self.sclt()
        l132 = l0 / 3 
        n132 = 1
        e132 = l132 / n132
        
        while e132 > sclt:
            n132 = n132 + 1
            e132 = l132 / n132
        
        return [n132, e132*100, l0/3*100]
                    
    def n1e1(self):
        diamBarreLongMax = self.diamBarreLongMax
        if (diamBarreLongMax >= 8) or (diamBarreLongMax <=14):
            return self.n11e11()
        if diamBarreLongMax > 14:
            return self.n12e12()
        if diamBarreLongMax >= 20:
            return [self.n131e131(), self.n132e132()]
    
    def n2e2(self):
        # Zone courante
        hsd = self.hsd
        scltmax = self.scltmax()
        lRepZoneRec = self.n1e1()[2] / 100
        lRepZoneCourante = hsd - 2 * lRepZoneRec
        n2 = 1
        e2 = lRepZoneCourante / n2
        
        while e2 > scltmax:
            n2 = n2 + 1
            e2 = lRepZoneCourante / n2
        
        return [n2, e2*100, lRepZoneCourante*100]
    
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
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    b = 40/100
    h = 18/100
    hsd = 286/100
    diamBarreLongMin = 8
    diamBarreLongMax = 8
    diamBarreTrans = 6
    nbBarreTrans = 3
    asReq = 1.44 / 1e4
    asProv = 3.02 / 1e4
    pot = PoteauDC(beton, acier, b, h, hsd, diamBarreLongMin, diamBarreLongMax, diamBarreTrans, nbBarreTrans, asReq, asProv)
    
    print(f"scltmax = {pot.scltmax()*100:.0f}")
    print(f"sclt = {pot.sclt()*100:.0f}")
    print(f"lbrqd = {pot.lbrqd()*100:.0f}")
    print(f"l0 = {pot.l0()*100:.0f}")
    # print(f"n11e11 = {pot.n11e11()}")
    # print(f"n1e1 = {pot.n1e1()}")
    # print(f"n2e2 = {pot.n2e2()}")
    # print(f"n131e131 = {pot.n131e131()}")
    # print(f"n132e132 = {pot.n132e132()}")
    
    print(f"n1 x e1 : {pot.n1e1()[0]:.0f} x {pot.n1e1()[1]:.0f}")
    print(f"n2 x e2 : {pot.n2e2()[0]:.0f} x {pot.n2e2()[1]:.0f}")
    print(f"n1 x e1 : {pot.n1e1()[0]:.0f} x {pot.n1e1()[1]:.0f}")