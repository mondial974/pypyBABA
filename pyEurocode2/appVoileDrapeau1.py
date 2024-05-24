from utilsprint import *
from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *

class VoileDrapeau1:
    
    def __init__(self, beton, acier, l, h, ep, FEd):
        self.beton = beton
        self.acier = acier
        self.l = l
        self.h = h
        self.ep = ep
        self.FEd = FEd
    
    def RAh(self):
        l = self.l
        h = self.h
        FEd = self.FEd
        return FEd * l / h
    
    def RAv(self):
        FEd = self.FEd
        return FEd
    
    def RBh(self):
        l = self.l
        h = self.h
        FEd = self.FEd
        return FEd * l / h
    
    def RBv(self):
        return 0
    
    def asTirant(self):
        RBh = self.RBh()
        fyd = self.acier.fyd()
        return RBh / fyd       
        
    def resultatLong(self):
        printentete()
        print("DONNÉES D'ENTRÉE")
        printfintab()
        # print("")
        print("Béton")
        printligne("Classe de résistance", "-", "-", f"{self.beton.classeresistance}")
        printligne("Résistance caractéritique en compression", "fck", "Mpa", f"{self.beton.fck()}")    
        printligne("Résistance de calcul en compression", "fcd", "Mpa", f"{self.beton.fck()}")   
        printligne("Coefficient de sécurité", "γc", "-", f"{self.beton.gamma_c}")   
        print("")
        print("Acier")
        printligne("Limite d'élasticité", "fyk", "MPa", f"{self.acier.fyk()}")
        printligne("Résistance de calcul", "fyd", "MPa", f"{self.acier.fyd():.0f}") 
        printligne("Coefficient de sécurité sur l'acier", "γs", "-", f"{self.acier.gamma_s}")  
        print("")
        print("Géométrie")
        printligne("Portée", "L", "cm", f"{self.l*100:.0f}")   
        printligne("Hauteur", "H", "cm", f"{self.h*100:.0f}")   
        printligne("Épaisseur voile", "ep", "cm", f"{self.ep*100:.0f}")   
        print("")
        print("Sollicitation")
        printligne("Effort vertical", "FEd", "T", f"{self.FEd*100:.2f}")   
        print("")
        printfintab()
        print("RÉSULTATS")
        printfintab()
        # print("")
        print("Noeud A")
        printligne("Réaction horizontale", "RAh", "T", f"{self.RAh()*100:.2f}")
        printligne("Réaction verticale", "RAv", "T", f"{self.RAv()*100:.2f}")
        print("")
        print("Noeud B")
        printligne("Réaction horizontale (effort dans le tirant)", "RBh", "T", f"{self.RBh()*100:.2f}")
        printligne("Réaction verticale", "RBv", "T", f"{self.RBv()*100:.2f}")
        printligne("Armatures tirant", "As tirant", "cm2", f"{self.asTirant()*1e4:.2f}")
          
if __name__ == "__main__":
    situation = SituationProjet("Durable")
    
    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1 
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    
    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    l = 300 / 100
    h = 600 / 100
    ep = 15 / 100
    FEd = 59.7 / 100
    
    vd1 = VoileDrapeau1(beton, acier, l, h, ep, FEd)
    vd1.resultatLong()