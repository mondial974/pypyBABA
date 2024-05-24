from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from appVerificationContrainteELS import *

# I0        : moment d'inertie de la section totale rendue homogène, calculé avec alpha_e = 15
# Sigma_s   : contrainte de traction effective de l'armatures, correspondant au cas de charge considéré, pour un moment évalué entre nu d'appuis
# As        : Section des armatures tendue
# rho       : Rapport de l'aire As de la section de l'armature tendue à l'aire de la section utile de la nervure bw.d
# bw        : largeur de la nervure
# beff      : Largeur de la table de compression

# Données d'entrée
# Mgi   : Moment instanné des charges permanentes 
# Mgv   : Moment differé des charges permanentes 
# Mji   : Moment instantanné des charges permanentes juste apres la pose des éléments fragiles
# Mpi   : Moment instantanné des charges permanente + charge d'exploitation
# ln    : portée entre nu
# bw    : largeur nervure
# beff  : largeur table de compression
# fck   : résistance du béton en compression
# Ecm   : Module de déformation instantané du béton
# Eceff : Module de déformation différé du béton
# As    : section d'armature mis en oeuvre

# Paramètre de calcul
# fctw
# rho
# lambda_v
# lambda_i
# mu
# Ifv
# Ifi
# fgi
# fgv
# fji
# Deltaft
# flim

# j : part de charges permamentes au moment de la mise en place des éléments fragiles
# pp : poids propre
# fr : élément fragile dans le cas où les éléments fragiles sont le premier élément fragiles et la première charge permanente posés
# per : dans ce cas l'ensemble des autres charges permamentes posées après l'élément fragile
# g : charge permanente totale (g > j), g = pp + fr + per
# p : charge permanenete g et d'exploitation q, p = g + q 

# j : charge permanente avant pose des éléments fragile
# fr : charge des éléments fragiles
# per : charge permanente appliqué apres les éléments fragiles


class Fleche:
    def __init__(self, beton, acier, type_travee, Mg, Mj, Mp, ln, bw, beff, h, c, As, Io):
        self.beton = beton
        self.acier = acier
        self.type_travee = type_travee
        self.Mg = Mg
        self.Mj = Mj
        self.Mp = Mp
        self.ln = ln
        self.bw = bw
        self.beff = beff
        self.h = h
        self.c = c
        self.As = As
        self.Io = Io
    
    def d(self):
        return self.h - self.c

    def isconsole(self):
        if self.type_travee == "Console":
            return True
        else:
            return False

    def fctw(self):
        if self.beton.fck() <= 60:
            return 0.06 * self.beton.fck() + 0.6
        else:
            return 0.275 * self.beton.fck()**(2./3.)

    def rho(self):
        return self.As / (self.bw * self.d())
    
    
###############################################################################
# Calcul des sigma_s
###############################################################################
    def sigma_s_g(self):
        beton = self.beton
        acier = self.acier
        Mser = self.Mg
        bw = self.bw
        beff = self.beff
        h = self.h
        hf = 0 / 100
        c1 = self.c
        c2 = 3 / 100
        As1 = self.As
        As2 = 0 / 1e4
        vc = VerifContrainteELSSectionRectangulaire(beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2)
        return vc.Ss1_rect_fissuree()

    def sigma_s_j(self):
        beton = self.beton
        acier = self.acier
        Mser = self.Mj
        bw = self.bw
        beff = self.beff
        h = self.h
        hf = 0 / 100
        c1 = self.c
        c2 = 3 / 100
        As1 = self.As
        As2 = 0 / 1e4
        vc = VerifContrainteELSSectionRectangulaire(beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2)
        return vc.Ss1_rect_fissuree()

    def sigma_s_p(self):
        beton = self.beton
        acier = self.acier
        Mser = self.Mp
        bw = self.bw
        beff = self.beff
        h = self.h
        hf = 0 / 100
        c1 = self.c
        c2 = 3 / 100
        As1 = self.As
        As2 = 0 / 1e4
        vc = VerifContrainteELSSectionRectangulaire(beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2)
        return vc.Ss1_rect_fissuree()


###############################################################################
# Calcul des lambda
###############################################################################
    def lambda_v(self):
        return 0.02 * self.fctw() / ((2 + 3 * self.bw / self.beff) * self.rho())

    def lambda_i(self):
        return 0.05 * self.fctw() / ((2 + 3 * self.bw / self.beff) * self.rho())


###############################################################################
# Calcul des mu
###############################################################################
    def mu_g(self):
        return max(1 - 1.75 * self.fctw() / (4 * self.sigma_s_g() * self.rho() + self.fctw()), 0)
    
    def mu_j(self):
        return max(1 - 1.75 * self.fctw() / (4 * self.sigma_s_j() * self.rho() + self.fctw()), 0)
    
    def mu_p(self):
        return max(1 - 1.75 * self.fctw() / (4 * self.sigma_s_p() * self.rho() + self.fctw()), 0)


###############################################################################
# Calcul des Inerties
###############################################################################
    def If_gi(self):
        return 1.1 * self.Io / (1 + self.lambda_i() * self.mu_g())
    
    def If_gv(self):
        return 1.1 * self.Io / (1 + self.lambda_v() * self.mu_g())
    
    def If_ji(self):
        return 1.1 * self.Io / (1 + self.lambda_i() * self.mu_j())
    
    def If_pi(self):
        return 1.1 * self.Io / (1 + self.lambda_i() * self.mu_p())


###############################################################################
#  Calcul des flèches
############################################################################### 
    def f_gi(self):
        """Flèche instatannée dues à l'ensemble des charges permamentes"""
        if self.isconsole():
            return self.Mg * self.ln**2 / (4 * self.beton.Ecm() * self.If_gi())
        else:
            return self.Mg * self.ln**2 / (10 * self.beton.Ecm() * self.If_gi())

    def f_gv(self):
        """Flèche différée dues à l'ensemble des charges permamentes"""
        if self.isconsole():
            return self.Mg * self.ln**2 / (4 * self.beton.Eceff() * self.If_gv())
        else:
            return self.Mg * self.ln**2 / (10 * self.beton.Eceff() * self.If_gv())
        
    def f_ji(self):  
        """Flèche instantannée dues aux charges permamentes appliquées à la fin de la mise en oeuvre du premier élément fragile"""
        if self.isconsole():
            return self.Mj * self.ln**2 / (4 * self.beton.Ecm() * self.If_ji())
        else:
            return self.Mj * self.ln**2 / (10 * self.beton.Ecm() * self.If_ji())
    
    def f_pi(self):
        """Flèche instantannée dues aux charges permamentes + exploitation"""
        if self.isconsole():
            return self.Mp * self.ln**2 / (4 * self.beton.Ecm() * self.If_pi())
        else:
            return self.Mp * self.ln**2 / (10 * self.beton.Ecm() * self.If_pi())

    def Delta_ft(self):
        return self.f_gv() - self.f_ji() + self.f_pi() - self.f_gi()

    def f_lim(self):
        if self.isconsole():
            if self.ln <= 2.5:
                return self.ln / 250
            else:
                return 0.005 + self.ln / 500
        else:
            if self.ln <= 5:
                return self.ln / 500
            else:
                return 0.005 + self.ln / 700

###############################################################################
#  Affichage des résultats
############################################################################### 
    def resultat_long(self):
        printentete()
        printligne("-", "Ecm", "", f"{self.beton.Ecm():.2f}")
        printligne("-", "Eceff", "", f"{self.beton.Eceff():.2f}")
        printligne("-", "fctw", "", f"{self.fctw():.2f}")
        printligne("-", "rho", "", f"{self.rho()*100:.2f}")
        print("")
        printligne("-", "sigma_s_g", "", f"{self.sigma_s_g():.2f}")
        printligne("-", "sigma_s_j", "", f"{self.sigma_s_j():.2f}")
        printligne("-", "sigma_s_p", "", f"{self.sigma_s_p():.2f}")
        print("")
        printligne("-", "lambda_i", "", f"{self.lambda_i():.2f}")
        printligne("-", "lambda_v", "", f"{self.lambda_v():.2f}")
        print("")
        printligne("-", "mu_g", "", f"{self.mu_g():.2f}")
        printligne("-", "mu_j", "", f"{self.mu_j():.2f}")
        printligne("-", "mu_p", "", f"{self.mu_p():.2f}")
        print("")
        printligne("-", "If_gi", "", f"{self.If_gi()}")
        printligne("-", "If_gv", "", f"{self.If_gv()}")
        printligne("-", "If_ji", "", f"{self.If_ji()}")
        printligne("-", "If_pi", "", f"{self.If_pi()}")

        print("")

        printligne("-", "fgi", "mm", f"{self.f_gi()*1000:.1f}")
        printligne("-", "fgv", "mm", f"{self.f_gv()*1000:.1f}")
        printligne("-", "fji", "mm", f"{self.f_ji()*1000:.1f}")
        printligne("-", "fpi", "mm", f"{self.f_pi()*1000:.1f}")
        printligne("fleche nuisible", "fnui", "mm", f"{self.Delta_ft()*1000:.1f}")
        printligne("fleche limite", "flim", "mm", f"{self.f_lim()*1000:.1f}")

    def resultat_court(self):
        pass
            

###############################################################################
#  TEST
############################################################################### 
if __name__ == "__main__":
    situation = "Durable"
    situation = SituationProjet(situation)
        
    classeexposition = "XC3"
    classeresistance = "C30/37"
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

    type_travee = "Poutre"
    Mg = 1.21 / 100
    Mj = 1.21 / 100
    Mp = 1.39/ 100
    ln = 239 / 100
    bw = 100 / 100
    beff = 100 / 100
    h = 20 / 100
    c = 3 / 100
    As = 2.63 / 1e4
    Io = bw * h**3 / 12
    fleche = Fleche(beton, acier, type_travee, Mg, Mj, Mp, ln, bw, beff, h, c, As, Io)
    fleche.resultat_long()