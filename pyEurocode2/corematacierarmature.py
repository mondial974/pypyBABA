from math import pi
from rich.table import Table
from rich.console import Console
from pyEurocode2.coreconstante import *
from pyEurocode2.coresituationprojet import *
from pyEurocode2.utilsprint import *


class AcierArmature:
    
    def __init__(self, situation, nuance, diagramme, diametre):
        self.situation = situation
        self.nuance = nuance
        self.diagramme = diagramme
        self.diametre = diametre / 1000
        self.gamma_s = self.situation.gamma_s()


###############################################################################
# DEFINITION DES IS
###############################################################################
    def isdiagrammePI(self):
        diagramme = self.diagramme
        #---
        if diagramme == "Palier incliné":
            return True
        else:
            return False

###############################################################################
# CARACTERISTIQUES DES BARRES D'ARMATURES
###############################################################################
    def aire_barre(self):
        """Section d'une barre"""
        diametre = self.diametre
        #---
        aire_barre = pi * diametre**2. / 4.
        return aire_barre
    
    def perimetre_barre(self):
        """Périmètre d'une barre"""
        diametre = self.diametre
        #---
        perimetre_barre = pi * self.diametre
        return perimetre_barre
    
    def masse_lineaire_barre(self):
        """Masse linéaire d'une barre"""
        aire_barre = self.aire_barre()
        #---
        masse_lineaire_barre = aire_barre * RHO_ACIER 
        return masse_lineaire_barre
    
    def As_nb_diametre(self, nb):
        return self.aire_barre() * nb

       
###############################################################################
# RESISTANCES
###############################################################################    
    def fyk(self):
        """Limite d'élasticité de l'acier"""
        nuance = self.nuance
        #---
        fyk = DICT_FYK[nuance]
        return fyk

    def fyd(self):
        """Résistance de calcul de l'acier"""
        fyk = self.fyk()
        gamma_s = self.situation.gamma_s()
        #---
        fyd = fyk / gamma_s
        return fyd
    
    def fywd(self):
        fyd = self.fyd()
        #---
        fywd = fyd
        return fywd
    
    def Ss_bar_comb_car(self):
        fyk = self.fyk()
        #---
        Ss_bar_comb_car = 0.8 * fyk
        return Ss_bar_comb_car
    
    def Ss_bar_dep_imp(self):
        fyk = self.fyk()
        #---
        Ss_bar_dep_imp = fyk
        return Ss_bar_dep_imp


###############################################################################
# DUCTILITE
###############################################################################
    def classe_ductilite(self):
        """Classe de ductilité"""
        nuance = self.nuance
        #---
        classe_ductilite = DICT_DUCTILITE[nuance]
        return classe_ductilite
    
    def k(self):
        classe_ductilite = self.classe_ductilite()
        #---
        k = DICT_K[classe_ductilite]
        return k


###############################################################################
# ALLONGEMENTS
###############################################################################
    def epsilon_uk(self):
        classe_ductilite = self.classe_ductilite()
        #---
        epsilon_uk = DICT_EPSILON_UK[classe_ductilite]
        return epsilon_uk
 
    def epsilon_ud(self):
        epsilon_uk = self.epsilon_uk()
        #---
        epsilon_ud = 0.9 * epsilon_uk  
        return epsilon_ud
            
    def epsilon_yd(self):
        fyd = self.fyd()
        #---
        epsilon_yd = self.fyd() / ES
        return epsilon_yd
    

###############################################################################
# RELATIONS CONTRAINTE DEFORMATION
###############################################################################
    def Ss_PH(self, epsilon_s):
        """Relation contrainte déformation Diagramme palier horizontal"""
        self.epsilon_s = epsilon_s
        epsilon_s = self.epsilon_s
        epsilon_yd = self.epsilon_yd()
        fyd = self.fyd()
        #---
        if epsilon_s > epsilon_yd:
            Ss_PH = fyd
        else:
            Ss_PH = ES * epsilon_s
        return Ss_PH
    
    def Ss_PI(self, epsilon_s):
        """Relation contrainte déformation Diagramme palier incliné"""
        self.epsilon_s = epsilon_s
        epsilon_s = self.epsilon_s
        epsilon_yd = self.epsilon_yd()
        fyd = self.fyd()
        k = self.k()
        epsilon_uk = self.epsilon_uk()
        #---
        if epsilon_s > epsilon_yd:
            a = (1 - fyd * (k - 1) / (ES * epsilon_uk - fyd)) * fyd
            b = fyd * (k - 1) / (epsilon_uk - fyd / ES)
            Ss_PI = a + b * self.epsilon_s
        else:
            Ss_PI =  ES * epsilon_s
        return Ss_PI
            
    def eq_SS_PI(self):
        fyd = self.fyd()
        k = self.k()
        epsilon_uk = self.epsilon_uk()
        epsilon_ud = self.epsilon_ud()
        #---
        a = (1 - fyd * (k - 1) / (ES * epsilon_uk - fyd)) * fyd
        b = fyd * (k - 1) / (epsilon_uk - fyd / ES)
        Sslim = self.Ss_PI(epsilon_ud)
        return print(f"Ssbar = {a:.2f} + {b:.2f} * epsilon_s, limité à {Sslim:.0f} MPa")
    

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
        printligne("Classe de ductilité", "-", "-", f"{self.classe_ductilite()}")
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
        printligne("Coefficient de sécurité sur l'acier", "gamma_s", "-", f"{self.situation.gamma_s()}")    
        printligne("Résistance de calcul", "fyd", "MPa", f"{self.fyd():.0f}") 
        printsep()
        print("Résistance de calcul à ELS")  
        printligne("Sous combinaison caractéristique", "0,8.fyk", "MPa", f"{self.Ss_bar_comb_car():.0f}")   
        printligne("Sous déformation imposée", "1.fyk", "MPa", f"{self.Ss_bar_dep_imp():.0f}") 
        printsep()
        print("Caractéristique de la barre")  
        printligne("Masse volumique acier", "rho_acier", "kg/m3", f"{RHO_ACIER}")
        printligne("Diamètre", "D", "mm", f"{self.diametre*1000:.0f}")
        printligne("Section", "aire_barre", "cm2", f"{self.aire_barre()*1e4:.2f}") 
        printligne("Masse linéaire", "M", "kg/ml", f"{self.masse_lineaire_barre():.3f}") 
        printligne("Périmètre", "P", "mm", f"{self.perimetre_barre()*1000:.2f}") 
        printfintab()       
        self.eq_SS_PI()


###############################################################################
# TEST
###############################################################################
if __name__ == "__main__":
    situation = SituationProjet("Durable")
    nuance = "S400C"
    diagramme = "Palier horizontal"
    diametre = 0
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    acier.resultat_long()