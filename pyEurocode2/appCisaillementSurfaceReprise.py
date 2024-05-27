from math import radians, sin, cos
from coreconstante import *
from coresituationprojet import *
from utilsmath import *
from utilsprint import *
from corematbetonarme import *
from corematacierarmature import *

C = 0.40
MU = 0.70

class SurfaceReprise():
    
    def __init__(self, beton, acier, VEd, z, bi, beta, As, alpha, sigma_n) -> None:
        self.beton = beton
        self.acier = acier
        self.VEd = VEd
        self.z = z
        self.bi = bi
        self.beta = beta
        self.As = As
        self.alpha = alpha
        self.sigma_n = sigma_n
        
        
###############################################################################
# CALCUL DES CONTRAINTES DE CISAILLEMENT
###############################################################################
    def vEdi(self):
        beta = self.beta
        VEd = self.VEd
        z = self.z
        bi = self.bi
        return beta * VEd / (z * bi)
    
    def vRdi(self):
        fctd = self.beton.fctd()
        fcd = self.beton.fcd()
        fyd = self.acier.fyd()
        alpha = radians(self.alpha)
        sigma_n = self.sigma_n
        rho = self.rho()
        nu = self.nu()
                
        vRdi1 = C * fctd + MU * sigma_n + rho * fyd * (MU * sin(alpha) + cos(alpha))
        vRdi2  = 0.5 * nu * fcd
        return min(vRdi1, vRdi2)
        
    
###############################################################################
# AIRE CISAILLEE ET RATIO D'ACIER TRAVERSANT CETTE AIRE
###############################################################################      
    def Ai(self):
        bi = self.bi
        z = self.z
        return bi * z
    
    def rho(self):
        As = self.As
        Ai = self.Ai()
        return As / Ai
    
    
###############################################################################
# VALEUR DE nu
###############################################################################    
    def nu(self):
        """Coefficient de réduction nu de la résistance du béton fissuré en cisaillement"""
        fck = self.beton.fck()
        return 0.6 * (1. - fck / 250.)


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
        vEdi = self.vEdi()
        vRdi = self.vRdi()
                        
        if vEdi <= vRdi:
            print(f"vEdi = {vEdi:.2f} MPa <= vRdi = {vRdi:.2f} MPa ==> VÉRIFIÉ")
        else:
            print(f"vEdi = {vEdi:.2f} MPa > vRdi = {vRdi:.2f} MPa ==> NON VÉRIFIÉ")
        

if __name__ == "__main__":
    situation = "Durable"
    s = SituationProjet(situation)
    
    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    alpha_e = 15
    fiinft0 = 2
    b = BetonArme(s, classeexposition, classeresistance, acc, act, age, classeciment, alpha_e, fiinft0)
    
    nuance = "S500B"
    diagramme = "Palier horizontal"
    diametre = 8
    a = AcierArmature(s, nuance, diagramme, diametre)
    
    
    VEd = 30.4 / 100
    z = 60 / 100
    bi = (2 * 38 + 2 * 54) / 100
    beta = 1
    As = 0 / 1e4
    alpha = 90
    sigma_n = 0 / 100
    surface = SurfaceReprise(b, a, VEd, z, bi, beta, As, alpha, sigma_n)
    
    surface.resultat_court()