#from colorama import Fore, Style
from math import radians, tan, sqrt, sin
#from rich.table import Table
#from rich.console import Console
from coreconstante import *
from coresituationprojet import *
from utilsmath import *
from utilsprint import *
from corematbetonarme import *
from corematacierarmature import *


class EffortTranchant():
    
    def __init__(self, beton, acier, redistribution, VEdmax, VEdred, NEd, bw, h, c1, Asl, Asw, s, alpha, teta) -> None:
        self.beton = beton
        self.acier = acier
        self.redistribution = redistribution
        self.VEdmax = VEdmax
        self.VEdred = VEdred
        self.NEd = NEd
        self.bw = bw
        self.h = h
        self.c1 = c1
        self.Asl = Asl
        self.Asw = Asw
        self.s = s
        self.alpha = radians(alpha)
        self.teta = radians(teta)
        

###############################################################################
# DEFINITION DES IS
###############################################################################
    def isArmatureEffortTranchantRequis(self):
        VEdmax = self.VEdmax
        VRdc = self.VRdc()
        if VEdmax > VRdc:
            return True
        else:
            return False
        
        
###############################################################################
# CARACTERISTIQUE GEOMETRIE
###############################################################################
    def Ac(self):
        """Section de béton"""
        bw = self.bw
        h = self.h
        return bw * h
    
    def d(self):
        """Hauteur utile"""
        h = self.h
        c1 = self.c1
        return h - c1
    
    def z(self):
        """Bras de levier"""
        d = self.d()
        return 0.9 * d
    
    
###############################################################################
# CARACTERISTIQUE ARMATURES D'EFFORTS TRANCHANT
###############################################################################
    def fywd(self):
        """Limite d'élasticité des armatures d'efforts tranchants"""
        fyd = self.acier.fyd()
        return fyd
        

###############################################################################
# VALEUR DE nu
###############################################################################
    def nu_min(self):
        """Coefficient de réduction nu_min de la résistance du béton fissuré en cisaillement"""
        redistribution = self.redistribution
        fck = self.beton.fck()
        k = self.k()
        dict_vmin = {"Dalle": 0.23 * sqrt(fck),
                     "Poutre": 0.035 * k**3./2. * sqrt(fck),
                     "Voile": 0.23 * sqrt(fck)}
        return dict_vmin[redistribution]

    def nu_1(self):
        """Coefficient de réduction nu_1 de la résistance du béton fissuré en cisaillement"""
        fck = self.beton.fck()
        return 0.6 * (1. - fck / 250.)

    def nu(self):
        """Coefficient de réduction nu de la résistance du béton fissuré en cisaillement"""
        fck = self.beton.fck()
        return 0.6 * (1. - fck / 250.)
    
    
###############################################################################
# VALEUR DE k
###############################################################################
    def k1(self):
        """Coefficient k1"""
        return 0.15

    def k(self):
        """Coefficient k"""
        d = self.d() * 1000.
        k1 = 1 + sqrt(200. / d)
        k2 = 2
        k = min(k1, k2)
        return k
    

###############################################################################
# CALCUL DE VRdc
###############################################################################
    def CRdc(self):
        """Valeur CRdc"""
        gamma_c = self.beton.gamma_c
        return 0.18 / gamma_c
    
    def sigma_cp(self):
        """Contrainte de compression"""
        NEd = self.NEd
        Ac = self.Ac()
        fcd = self.beton.fcd()
        sigma_cp1 = NEd / Ac
        sigma_cp2 = 0.2 * fcd
        return min(sigma_cp1, sigma_cp2)
       
    def VRdc1(self):
        """Composante 1 de l'équation de l'effort tranchant résistant VRdc"""
        CRdc = self.CRdc()
        k = self.k()
        k1 = self.k1()
        rho_l = self.rho_l()
        sigma_cp = self.sigma_cp()
        bw = self.bw
        d = self.d()
        fck = self.beton.fck()
        return (CRdc * k * (100. * rho_l * fck)**(1./3.) + k1 * sigma_cp) * bw * d
    
    def VRdc2(self):
        """Composante 2 de l'équation de l'effort tranchant résistant VRdc"""
        vmin = self.nu_min()
        k1 = self.k1()
        bw = self.bw
        d = self.d()
        sigma_cp = self.sigma_cp()
        return (vmin + k1 * sigma_cp) * bw * d
    
    def VRdc(self):
        """Effort tranchant résistant"""
        VRdc1 = self.VRdc1()
        VRdc2 = self.VRdc2()
        return max(VRdc1, VRdc2)
    
###############################################################################
# CALCUL DE VRdc,max
###############################################################################
    def alpha_cw(self):
        """Coefficient tenant compte de l'état de contrainte dans la menbrure comprimée"""
        return 1.
    
    def VRdmax1(self):
        """Effort tranchant maximal admissible avant écrasement des bielles dans le cas où les armatures d'efforts tranchant ne sont pas requis"""
        bw = self.bw
        d= self.d()
        nu = self.nu()
        fcd = self.beton.fcd()
        return 0.5 * bw * d * nu * fcd
    
    def VRdmax2(self):
        """Effort tranchant maximal admissible avant écrasement des bielles dans le cas où les armatures d'efforts tranchant sont requis"""
        alpha_cw = self.alpha_cw()
        bw = self.bw
        z = self.z()
        nu_1 = self.nu_1()
        fcd = self.beton.fcd()
        teta = self.teta
        alpha = self.alpha
        return alpha_cw * bw * z * nu_1 * fcd * (cot(teta) + cot(alpha)) / (1 + (cot(teta))**2)
            
    def VRdmax(self):
        VRdmax1 = self.VRdmax1()
        VRdmax2 = self.VRdmax2()    
        if self.isArmatureEffortTranchantRequis():
            return VRdmax2
        else:
            return VRdmax1
       

###############################################################################
# CALCUL DE VRds
###############################################################################
    def VRds(self):
        teta = self.teta
        alpha = self.alpha
        z = self.z()
        fywd = self.fywd()
        Asw = self.Asw
        s = self.s
        Asw_s_reel = self.Asw_s_reel()
        alpha = self.alpha
        return Asw_s_reel * z * fywd * (cot(teta) + cot(alpha)) * sin(alpha)
           
    
###############################################################################
# RATIO ARMATURES LONGITUDINALES
###############################################################################    
    def rho_l(self):
        Asl = self.Asl
        bw = self.bw
        d = self.d()
        rho_l1 = Asl / (bw * d)
        rho_l2 = 2. / 100.
        return min(rho_l1, rho_l2)
    
    
###############################################################################
# RATIO ARMATURES TRANSVERSALES
###############################################################################       
    def rho_wmin(self):
        fck = self.beton.fck()
        fyk = self.acier.fyk()
        return 0.08 * sqrt(fck) / fyk
        
    def rho_w(self):
        Asw_s = self.Asw_s_reel()
        bw = self.bw
        alpha = self.alpha
        return Asw_s / (bw * sin(alpha))
    
    def rho_wmax(self):
        Asw_s_max = self.Asw_s_max()
        bw = self.bw
        alpha = self.alpha
        return Asw_s_max / (bw * sin(alpha))

###############################################################################
# RATIO ARMATURES TRANSVERSALES
############################################################################### 
    def Asw_s_reel(self):
        Asw = self.Asw
        s = self.s
        if Asw == 0 or s == 0:
            return 0
        else:
            return Asw / s
    
    def Asw_s_th(self):
        VEdred = self.VEdred
        fywd = self.fywd()
        teta = self.teta
        alpha = self.alpha
        z = self.z()
        asw_s1 = self.Asw_s_min()
        asw_s2 = VEdred / (z * fywd * (cot(teta) + cot(alpha)) * sin(alpha))
        return max(asw_s1, asw_s2)
    
    def Asw_s_min(self):
        rho_wmin = self.rho_wmin()
        bw = self.bw
        alpha = self.alpha
        return rho_wmin * bw * sin(alpha)      
    
    def Asw_s_max(self):
        alpha_cw = self.alpha_cw()
        nu_1 = self.nu_1()
        fcd = self.beton.fcd()
        bw = self.bw
        alpha = self.alpha
        fywd = self.fywd()
        return 0.5 * alpha_cw * nu_1 * fcd * bw / (sin(alpha) * fywd) 

###############################################################################
# EFFORT DE TRACTION SUPPLEMENTAIRE
############################################################################### 
    def DeltaFtd(self):
        VEd = self.VEdmax
        teta = self.teta
        alpha = self.alpha
        return 0.5 * VEd * (cot(teta) - cot(alpha))


###############################################################################
# AFFICHAGE DES RESULTATS
###############################################################################  
    def resultat_long(self):
        Asw_s_reel = self.Asw_s_reel()
        self.resultat_court()
        print("")
        printentete()
        print("Béton")
        printligne("-", "fck", "MPa", f"{self.beton.fck():.2f}")
        printligne("-", "fcd", "MPa", f"{self.beton.fcd():.2f}")
        print("Acier de béton armé")
        printligne("-", "fyk", "MPa", f"{self.acier.fyk():.0f}")
        printligne("-", "fyd", "MPa", f"{self.acier.fyd():.0f}")
        printligne("-", "fywd", "MPa", f"{self.fywd():.0f}")
        print("Sollicitation")
        printligne("Effort tranchant max", "VEdmax", "T", f"{self.VEdmax*100:.2f}")
        printligne("Effort tranchant réduit", "VEdred", "T", f"{self.VEdred*100:.2f}")
        printligne("Effort de compression", "NEd", "T", f"{self.NEd*100:.2f}")
        print("Géométrie")
        printligne("Largeur", "bw", "cm", f"{self.bw*100:.2f}")
        printligne("Hauteur", "h", "cm", f"{self.h*100:.2f}")
        printligne("Enrobage", "c1", "cm", f"{self.c1*100:.2f}")
        printligne("Hauteur utile", "d", "cm", f"{self.d()*100:.2f}")
        printligne("Bras de levier", "z", "cm", f"{self.z()*100:.2f}")
        print("Paramètres de calcul")
        printligne("-", "CRdc", "MPa", f"{self.CRdc():.2f}")
        printligne("-", "k", "-", f"{self.k():.2f}")
        printligne("-", "k1", "-", f"{self.k1():.2f}")
        printligne("-", "rho_l", "%", f"{self.rho_l()*100:.2f}")
        printligne("-", "sigma_cp", "MPa", f"{self.sigma_cp():.2f}")
        printligne("-", "nu_min", "-", f"{self.nu_min():.2f}")
        printligne("-", "nu", "-", f"{self.nu():.2f}")
        printligne("-", "nu_1", "-", f"{self.nu_1():.2f}")
        printligne("-", "alpha_cw", "-", f"{self.alpha_cw():.2f}")
        print("Efforts résistants")
        printligne("-", "VRdc", "T", f"{self.VRdc()*100:.2f}")
        printligne("-", "VRdmax", "T", f"{self.VRdmax()*100:.2f}")
        printligne("-", "VRds", "T", f"{self.VRds()*100:.2f}")
        print("Armatures d'effort tranchant")
        printligne("-", "rho_wmin", "%", f"{self.rho_wmin()*100:.2f}")
        printligne("-", "rho_w", "%", f"{self.rho_w()*100:.2f}")
        printligne("-", "rho_wmax", "%", f"{self.rho_wmax()*100:.2f}")
        printligne("-", "Asw_s_min", "cm2/cm", f"1 / {1/self.Asw_s_min() / 100:.2f}")
        printligne("-", "Asw_s_max", "cm2/cm", f"1 / {1/self.Asw_s_max() / 100:.2f}")
        printligne("-", "Asw_s_th", "cm2/cm", f"1 / {1/self.Asw_s_th() / 100:.2f}")
        if Asw_s_reel != 0:
            printligne("-", "Asw_s_reel", "cm2/cm", f"1 / {1/self.Asw_s_reel() / 100:.2f}")
        else:
            printligne("-", "Asw_s_reel", "cm2/cm", "0.00")
            
        
        
    def resultat_court(self):
        VEdmax = self.VEdmax
        VEdred = self.VEdred
        VRdmax = self.VRdmax()
        VRdc = self.VRdc()
        VRds = self.VRds()
        Asw_s_reel = self.Asw_s_reel()
        Asw_s_min = self.Asw_s_min()
        Asw_s_max = self.Asw_s_max()
                
        if VEdred <= VRdc:
            printMESSAGE(f"VEdred = {self.VEdred*100:.2f} T <= VRdc = {self.VRdc()*100:.2f} T ==> ARMATURES TRANCHANT NON REQUIS")
        
        if VEdred > VRdc:
            printMESSAGE(f"VEdred = {self.VEdred*100:.2f} T > VRdc = {self.VRdc()*100:.2f} T ==> ARMATURES TRANCHANT REQUIS")
            
        if VEdmax <= VRdmax:
            printVERIFIE(f"VEdmax = {self.VEdmax*100:.2f} T <= VRdmax = {self.VRdmax()*100:.2f} T")
        else:
            printNONVERIFIE(f"VEdmax = {self.VEdmax*100:.2f} T > VRdmax = {self.VRdmax()*100:.2f} T")
        
        if  VEdred <= VRds:
            printVERIFIE(f"VEdred = {self.VEdred*100:.2f} T <= VRds = {self.VRds()*100:.2f} T")
        else:
            printNONVERIFIE(f"VEdred = {self.VEdred*100:.2f} T > VRds = {self.VRds()*100:.2f} T")
        
        if Asw_s_reel != 0:       
            if Asw_s_reel < Asw_s_min:
                printNONVERIFIE(f"Asw/s reel = 1 / {1/Asw_s_reel / 100:.0f} cm2/cm < Asw/s_min = 1 / {1/Asw_s_min / 100:.0f} cm2/cm")
            
            if Asw_s_min <= Asw_s_reel and Asw_s_reel <= Asw_s_max:
                printVERIFIE(f"Asw/s_min = 1 / {1/Asw_s_min / 100:.0f} <= Asw/s reel = 1 / {1/Asw_s_reel / 100:.0f} cm2/cm <= Asw/s_max = 1 / {1/Asw_s_max / 100:.0f} cm2/cm")

            if Asw_s_reel > Asw_s_max:
                printNONVERIFIE(f"Asw/s reel = 1 / {1/Asw_s_reel / 100:.0f} cm2/cm > Asw/s_max = 1 / {1/Asw_s_max / 100:.0f} cm2/cm")    
        else:
            printNONVERIFIE("Asw/s réel = 0.00 cm2/cm")
        

if __name__ == "__main__":
    situation = "Durable"
    s = SituationProjet(situation)
    
    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    b = BetonArme(s, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    
    nuance = "S500B"
    diagramme = "Palier horizontal"
    diametre = 8
    a = AcierArmature(s, nuance, diagramme, diametre)
    
    redistribution = "Poutre"
    VEdmax = 19 / 100
    VEdred = 19 / 100
    NEd = 0 / 100
    bw = 84 / 100
    h = 60 / 100
    c1 = 5 / 100
    Asl = 0 / 1e4
    Asw = 1 / 1e4
    s = 15 / 100
    alpha = 45
    teta = 45
    ef = EffortTranchant(b, a, redistribution, VEdmax, VEdred, NEd, bw, h, c1, Asl, Asw, s, alpha, teta)
    
    ef.resultat_long()