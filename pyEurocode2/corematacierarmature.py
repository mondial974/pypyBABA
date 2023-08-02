from math import pi
from rich.table import Table
from rich.console import Console
from coreconstante import *
from coresituationprojet import *
from utilsprint import *

ES = 200000
RHO_ACIER = 7850

class AcierArmature:
    
    def __init__(self, situation, nuance, diagramme, diametre):
        self.situation = situation
        self.nuance = nuance
        self.diagramme = diagramme
        self.diametre = diametre / 1000


###############################################################################
# DEFINITION DES IS
###############################################################################
    def isdiagrammePI(self):
        if self.diagramme == "Palier incliné":
            return True
        else:
            return False

###############################################################################
# CARACTERISTIQUES DES BARRES D'ARMATURES
###############################################################################
    def An(self):
        """Diamètre d'une barre"""
        return pi * self.diametre**2 / 4
    
    def P(self):
        """Périmètre d'une barre"""
        return pi * self.diametre
    
    def masselineaire(self):
        """Masse linéaire d'une barre"""
        return self.An() * RHO_ACIER 

       
###############################################################################
# RESISTANCES
###############################################################################    
    def fyk(self):
        """Limite d'élasticité de l'acier"""
        dict_fyk = {"S500A" : 500, "S500B" : 500, "S500C" : 500,
                    "S400A" : 400, "S400B" : 400, "S400C" : 400}
        return dict_fyk[self.nuance]

    def fyd(self):
        """Résistance de calcul de l'acier"""
        return self.fyk() / self.situation.gs()
    
    def fywd(self):
        return self.fyd()
    
    def Ss_bar_comb_car(self):
        return 0.8 * self.fyk()
    
    def Ss_bar_dep_imp(self):
        return self.fyk()


###############################################################################
# DUCTILITE
###############################################################################
    def classeductilite(self):
        """Classe de ductilité"""
        dict_fyk = {"S500A" : "A", "S500B" : "B", "S500C" : "C",
                    "S400A" : "A", "S400B" : "B", "S400C" : "C"}
        return dict_fyk[self.nuance]
    
    def k(self):
        dict_k = { "A" : 1.05, "B" : 1.08, "C" : 1.15}
        return dict_k[self.classeductilite()]


###############################################################################
# ALLONGEMENTS
###############################################################################
    def epsilon_uk(self):
        dict_k = { "A" : 2.5 / 100, "B" : 5 / 100, "C" : 7.5 / 100}
        return dict_k[self.classeductilite()]    
    
    def epsilon_ud(self):
        return 0.9 * self.epsilon_uk()    
            
    def epsilon_yd(self):
        return self.fyd() / ES
    

###############################################################################
# RELATIONS CONTRAINTE DEFORMATION
###############################################################################
    def Ss_PH(self, es):
        """Relation contrainte déformation Diagramme palier horizontal"""
        self.es = es
        es = self.es
        eyd = self.epsilon_yd()
        fyd = self.fyd()
        
        if es > eyd:
            return fyd
        else:
            return ES * es
    
    def Ss_PI(self, es):
        """Relation contrainte déformation Diagramme palier incliné"""
        self.es = es
        es = self.es
        eyd = self.epsilon_yd()
        fyd = self.fyd()
        k = self.k()
        euk = self.epsilon_uk()
        
        if es > eyd:
            a = (1 - fyd * (k - 1) / (ES * euk - fyd)) * fyd
            b = fyd * (k - 1) / (euk - fyd / ES)
            return a + b * self.es
        else:
            return ES * es
            
    def eq_SS_PI(self):
        fyd = self.fyd()
        k = self.k()
        euk = self.epsilon_uk()
        eud = self.epsilon_ud()
        a = (1 - fyd * (k - 1) / (ES * euk - fyd)) * fyd
        b = fyd * (k - 1) / (euk - fyd / ES)
        Sslim = self.Ss_PI(eud)
        return f"Ssbar = {a:.2f} + {b:.2f} *, limité à {Sslim:.0f} MPa"
    

###############################################################################
# AFFICHAGE DES RESULTATS
###############################################################################
    def resultat_long(self):
        printentete()   
        print("Situation de projet")
        printligne("-", "-", "-", f"{self.situation.situation}")
        printsep()
        print("Armatures")
        printligne("Nuance armature", "-", "-", f"{self.nuance}")
        printligne("Limite d'élasticité", "fyk", "MPa", f"{self.fyk()}")
        printligne("Classe de ductilité", "-", "-", f"{self.classeductilite()}")
        printligne("Module de déformation", "Es", "MPa", f"{ES}")
        printsep()
        if self.isdiagrammePI():
            print("Diagramme à palier incliné")
            printligne("Coefficient k = (ft/fy)k", "k", "-", f"{self.k()}")
            printligne("Limite d'allongement linéaire", "epsilon_yd", "%", f"{self.epsilon_yd()*100:.4f}")
            printligne("Limite de déformation", "epsilon_ud", "%", f"{self.epsilon_ud()*100:.2f}")
            printligne("Allongement caractéristique", "epsilon_uk", "%", f"{self.epsilon_uk()*100:.2f}")
            print(f"    Equation du palier incliné : {self.eq_SS_PI()}")
        else:
            print("Diagramme à palier horizontal")
            printligne("Limite d'allongement linéaire", "epsilon_yd", "%", f"{self.epsilon_yd()*100:.4f}")
        printsep() 
        print("Résistance de calcul à l'ELU")  
        printligne("Coefficient de sécurité sur l'acier", "gs", "-", f"{self.situation.gs()}")    
        printligne("Résistance de calcul", "fyd", "MPa", f"{self.fyd():.0f}") 
        printsep()
        print("Résistance de calcul à ELS")  
        printligne("Sous combinaison caractéristique", "0,8.fyk", "MPa", f"{self.Ss_bar_comb_car():.0f}")   
        printligne("Sous déformation imposée", "1.fyk", "MPa", f"{self.Ss_bar_dep_imp():.0f}") 
        printsep()
        print("Caractéristique de la barre")  
        printligne("Masse volumique acier", "rho_acier", "kg/m3", f"{RHO_ACIER}")
        printligne("Diamètre", "D", "mm", f"{self.diametre*1000:.0f}")
        printligne("Section", "An", "cm2", f"{self.An()*1e4:.2f}") 
        printligne("Masse linéaire", "M", "kg/ml", f"{self.masselineaire():.3f}") 
        printligne("Périmètre", "P", "mm", f"{self.P()*1000:.2f}") 
        printfintab()       


###############################################################################
# TEST
###############################################################################
if __name__ == "__main__":
    situation = SituationProjet("Durable")
    nuance = "S500C"
    diagramme = "Palier horizontal"
    diametre = 0
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    # acier.resultat_long()