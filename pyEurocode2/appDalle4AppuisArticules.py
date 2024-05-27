# test

import numpy as np

from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from appFlexionSimpleSectionRectangulaire import *
from appVerificationContrainteELS import *
from coreDCdalle import *
from utilsmath import interpolation 
from fleche import *

ABAQUE = np.array([
       [0.50, 0.0965, 0.2584, 0.1215, 0.0999, 0.3830, 0.1167],
       [0.55, 0.0892, 0.2889, 0.1082, 0.0934, 0.4211, 0.1082],
       [0.60, 0.0820, 0.3289, 0.0998, 0.0869, 0.4682, 0.0998],
       [0.65, 0.0750, 0.3781, 0.0916, 0.0804, 0.5237, 0.0916],
       [0.70, 0.0683, 0.4388, 0.0838, 0.0742, 0.5831, 0.0838],
       [0.75, 0.0620, 0.5124, 0.0764, 0.0683, 0.6458, 0.0764],
       [0.80, 0.0561, 0.5964, 0.0694, 0.0627, 0.7115, 0.0694],
       [0.85, 0.0506, 0.6871, 0.0630, 0.0575, 0.7799, 0.0630],
       [0.90, 0.0456, 0.7845, 0.0571, 0.0527, 0.8510, 0.0571],
       [0.95, 0.0410, 0.8887, 0.0517, 0.0483, 0.9244, 0.0517],
       [1.00, 0.0368, 1.0000, 0.0468, 0.0442, 1.0000, 0.0468]
       ])

class Dalle4AppuisArticules:
        
    def __init__(self, situation, beton, acier, G, Q, AC, lx, ly, h, c):
        self.situation = situation
        self.beton = beton
        self.acier = acier
        self.G = G
        self.Q = Q
        self.AC = AC
        self.lx = lx
        self.ly = ly
        self.h = h
        self.c = c
        
    def a(self):
        """Calcul du rapport lx/ly"""
        return self.lx / self.ly
    
    def d(self):
        """Calcul de la hauteur utile"""
        return self.h - self.c
    
    def poids_propre_dalle(self):
        """Calcul du poids propre de la dalle"""
        return self.h * RHO_BETON_ARME/1e5
    

###############################################################################
# Calcul des chargement ELU et ELS
###############################################################################
# ELU
    def pu(self):
        """Calcul du chargement total ELU : Pu"""
        return 1.35 * (self.G + self.poids_propre_dalle()) + 1.5 * self.Q

# ELS
    def g(self):
        """Calcul de charges permanentes totales"""
        return self.G + self.poids_propre_dalle()
    
    def j(self):
        """Charge permanente après la pose des éléments fragiles"""
        return self.G + self.poids_propre_dalle() - self.AC

    def p(self):
        """Calcul du chargement total ELS : Pser"""
        return self.g() + self.Q
    

###############################################################################    
# Calcul des coefficients nu
###############################################################################
# pour coeffient de poisson = 0 
    def nux_elu(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][1]
                yb = ABAQUE[j+1][1]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
        
        if self.a() < 0.50:
            return 1/8  
        
        if self.a() == 0.50:
            return ABAQUE[0][1]
        
        if self.a() == 1:
            return ABAQUE[10][1]
    
    def nuy_elu(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][2]
                yb = ABAQUE[j+1][2]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
        
        if self.a() < 0.50:
            return 0   
                
        if self.a() == 0.50:
            return ABAQUE[0][2]
        
        if self.a() == 1:
            return ABAQUE[10][2]

# pour coeffient de poisson = 0.2    
    def nux_els(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][4]
                yb = ABAQUE[j+1][4]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
        
        if self.a() < 0.50:
            return 1/8  
        
        if self.a() == 0.50:
            return ABAQUE[0][4]
        
        if self.a() == 1:
            return ABAQUE[10][4]   
    
    def nuy_els(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][5]
                yb = ABAQUE[j+1][5]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
        
        if self.a() < 0.50:
            return 0  
                
        if self.a() == 0.50:
            return ABAQUE[0][5]
        
        if self.a() == 1:
            return ABAQUE[10][5] 
        
    def nuf_els(self):
        for j in range(0,10):            
            if ABAQUE[j][0] < self.a() <= ABAQUE[j+1][0]:
                xa = ABAQUE[j][0]
                xb = ABAQUE[j+1][0]
                ya = ABAQUE[j][6]
                yb = ABAQUE[j+1][6]
                x = self.a()
                return interpolation(xa, xb, ya, yb, x)
        
        if self.a() < 0.50:
            return 0.1563
                
        if self.a() == 0.50:
            return ABAQUE[0][6]
        
        if self.a() == 1:
            return ABAQUE[10][6]
        

###############################################################################
# Calcul des moments ELU et ELS
###############################################################################
# ELU
    def mx_elu(self):
        return self.nux_elu() * self.pu() * self.lx**2
    
    def my_elu(self):
        return self.nuy_elu() * self.mx_elu()

# ELS
    def mx_g(self):
        return self.nux_els() * self.g() * self.lx**2
    
    def mx_j(self):
        return self.nux_els() * self.j() * self.lx**2
    
    def mx_p(self):
        return self.nux_els() * self.p() * self.lx**2
    
    def my_els(self):
        return self.nuy_els() * self.mx_p()
    

###############################################################################
# Calcul de la flèche ELS
###############################################################################   
    def Io(self):
        beton = self.beton
        acier = self.acier
        Mser = 0
        bw = 100 / 100
        beff = 100 / 100
        h = self.h
        hf = 0 / 100
        c1 = self.c
        c2 = 3 / 100
        As1 = self.Asx_retenue()
        As2 = 0 / 1e4
        vc = VerifContrainteELSSectionRectangulaire(beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2)
        return vc.Ich_rect()
    
    def f_RDM_els(self):
        return self.nuf_els() * self.p() * self.lx**4 / (self.h**3 * self.beton.Eceff()) 
    
    def f_nui(self):
        type_travee = "Poutre"
        Mg = self.mx_g()
        Mj = self.mx_j()
        Mp = self.mx_p()
        ln = self.lx
        bw = 100 / 100
        beff = 100 / 100
        h = self.h
        c = self.c
        As = self.Asx_retenue()
        Io = self.Io()
        fleche = Fleche(self.beton, self.acier, type_travee, Mg, Mj, Mp, ln, bw, beff, h, c, As, Io)
        return fleche.Delta_ft()

    def f_lim(self):
        type_travee = "Poutre"
        Mg = self.mx_g()
        Mj = self.mx_j()
        Mp = self.mx_p()
        ln = self.lx
        bw = 100 / 100
        beff = 100 / 100
        h = self.h
        c = self.c
        As = self.Asx_retenue()
        Io = bw * h**3 / 12
        fleche = Fleche(self.beton, self.acier, type_travee, Mg, Mj, Mp, ln, bw, beff, h, c, As, Io)
        return fleche.f_lim()


 
###############################################################################   
# Calcul de Asx
###############################################################################
    def Asx_calc(self):
        beton = self.beton
        acier = self.acier
        bw = 100 / 100
        h = self.h
        c1 = self.c
        c2 = self.c
        Mu = self.mx_elu()
        Mser = self.mx_p()
        As2imposee = 0
        
        if self.mx_elu() == 0:
            Asx_calc = 0 
        else:
            fsrec = FlexionSimpleSectionRectangulaire(beton, acier, bw, h, c1, c2, Mu, Mser, As2imposee)
            Asx_calc = fsrec.As1()
        
        return Asx_calc
    
    def Asx_min_dalle(self):
        return 1.20 * self.Asx_calc()
    
    def Asx_min_poutre(self):
        bw = 100 / 100
        dcpoutre = DCPoutreRectangulaire(self.beton, self.acier, bw, self.h, self.c)
        return dcpoutre.Asmin()

    def Asx_retenue(self):
        Asmin = min(self.Asx_min_poutre(), self.Asx_min_dalle())
        return max(Asmin, self.Asx_calc())   
    

###############################################################################      
# Calcul de Asy
###############################################################################         
    def Asy_calc(self):
        beton = self.beton
        acier = self.acier
        bw = 100 / 100
        h = self.h
        c1 = self.c
        c2 = self.c
        Mu = self.my_elu()
        Mser = self.my_els()
        As2imposee = 0
            
        if self.my_elu() == 0:
            return 0
        else:
            fsrec = FlexionSimpleSectionRectangulaire(beton, acier, bw, h, c1, c2, Mu, Mser, As2imposee)
            Asy_calc = fsrec.As1()
         
        return Asy_calc
    
    def Asy_min_dalle(self):
        return 0.20 * self.Asx_calc()
    
    def Asy_retenue(self):
        return max(self.Asy_min_dalle(), self.Asy_calc())
    

###############################################################################
# Affichage des résultats
###############################################################################        
    def resultat_long(self):
        self.resultat_court()
        printentete()
        print("Situation de projet")
        printligne("    -", "-", "-", f"{self.situation.situation}")
        printsep()
        print("")
        print("Béton")
        printligne("    Classe de résistance", "-", "-", f"{self.beton.classeresistance}")
        printligne("    Résistance à la compression", "fck", "MPa", f"{self.beton.fck():.2f}")
        printligne("    Résistance de calcul", "fcd", "MPa", f"{self.beton.fcd():.2f}")
        printligne("    Résistance de calcul", "fcd", "MPa", f"{self.beton.fcd():.2f}")
        printligne("    Module de déformation", "Eceff", "MPa", f"{self.beton.Eceff():.2f}")
        printsep()
        print("")
        print("Acier pour armature")
        printligne("    Nuance", "-", "-", f"{self.acier.nuance}")
        printligne("    Limite d'élasticité", "fyk", "-", f"{self.acier.fyk():.0f}")
        printligne("    Résistance de calcul", "fyd", "-", f"{self.acier.fyd():.0f}")
        printsep()
        print("")
        print("Chargement uniforme")
        printligne("    Charge ELU", "Pu", "T/m2", f"{self.pu()*100:.2f}")
        printligne("    Charge ELS", "Pser", "T/m2", f"{self.p()*100:.2f}")
        printsep()
        print("")
        print("Géométrie")
        printligne("    Petit coté", "lx", "cm", f"{self.lx*100:.0f}")
        printligne("    Grand coté", "ly", "cm", f"{self.ly*100:.0f}")
        printligne("    Epaisseur", "h", "cm", f"{self.h*100:.0f}")
        printligne("    Enrobage", "c", "cm", f"{self.c*100:.0f}")
        print("")
        print("Moments ELU")
        printligne("    Coefficient", "nu_x", "-", f"{self.nux_elu():.4f}")
        printligne("    Coefficient", "nu_y", "-", f"{self.nuy_elu():.4f}")
        printligne("    Moment Mx", "Mx", "T.m", f"{self.mx_elu()*100:.2f}")
        printligne("    Moment My", "My", "T.m", f"{self.my_elu()*100:.2f}")
        print("Moments ELS")
        printligne("    Coefficient", "nu_x", "-", f"{self.nux_els():.4f}")
        printligne("    Coefficient", "nu_y", "-", f"{self.nuy_els():.4f}")
        printligne("    Moment Mx", "Mx", "T.m", f"{self.mx_p()*100:.2f}")
        printligne("    Moment My", "My", "T.m", f"{self.my_els()*100:.2f}")
        print("")
        print("Flèche")
        printligne("    Coefficient", "nu_f", "-", f"{self.nuf_els():.4f}")
        printligne("    Flèche ELS", "f_RDM_ELS", "mm", f"{self.f_RDM_els()*1000:.4f}")
        printfintab()
    
    def resultat_court(self):
        printligne("    Petit coté : portée de calcul", "lx", "cm", f"{self.lx*100:.0f}")
        printligne("    Grand coté : portée de calcul", "ly", "cm", f"{self.ly*100:.0f}")
        printligne("    Rapport des portées", "lx/ly", "-", f"{self.a():.2f}")
        print("")
        print("Armatures")
        printligne("    Armatures suivant x", "Asx", "cm2", f"{self.Asx_retenue()*1e4:.2f}")
        printligne("    Armatures suivant y", "Asy", "cm2", f"{self.Asy_retenue()*1e4:.2f}")
        print("")
        print("Moments ELU")
        printligne("    Moment Mx", "Mx", "T.m", f"{self.mx_elu()*100:.2f}")
        printligne("    Moment My", "My", "T.m", f"{self.my_elu()*100:.2f}")
        print("")
        print("Moments ELS")
        printligne("    Moment Mx", "Mx", "T.m", f"{self.mx_p()*100:.2f}")
        printligne("    Moment My", "My", "T.m", f"{self.my_els()*100:.2f}")
        print("")
        print("Flèche ELS")
        printligne("    Flèche ELS", "f_RDM", "mm", f"{self.f_RDM_els()*1000:.1f}")
        printligne("    Flèche nuisible", "f_nui", "mm", f"{self.f_nui()*1000:.1f}")
        printligne("    Flèche limite", "f_lim", "mm", f"{self.f_lim()*1000:.1f}")
        print("")   
    
    def minute(self):
        print("Données")     
        print("|Situation|Béton|Acier|G|AC|Q|lx|ly|h|c|")
        print("|--|--|--|--|--|--|--|--|--|--|")
        print(f"|{self.situation.situation}|{self.beton.classeresistance}|{self.acier.nuance}|{self.G*1e5:.0f}|{self.AC*1e5:.0f}|{self.Q*1e5:.0f}|{self.lx*100:.0f}|{self.ly*100:.0f}|{self.h*100:.0f}|{self.c*100:.1f}|")
        print("")
        print("Résultats")
        print("| |Mx|My|Asx|Asy|fnui|fadm|")
        print("|--|--|--|--|--|--|--|")
        print(f"|ELU|{self.mx_elu()*100:.2f}|{self.my_elu()*100:.2f}|{self.Asx_retenue()*1e4:.2f}|{self.Asy_retenue()*1e4:.2f}|{self.f_nui()*1000:.1f}|{self.f_lim()*1000:.1f}|")
        print(f"|ELS|{self.mx_p()*100:.2f}|{self.my_els()*100:.2f}|||||")


###############################################################################
# TEST
###############################################################################        
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
    
    G = 1200 / 1e5
    Q = 250 / 1e5
    AC = 0 / 1e5
    lx = 468 / 100
    ly = 700 / 100
    h = 25 / 100
    c = 3 / 100
    dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, lx, ly, h, c)
    dalle.resultat_court()