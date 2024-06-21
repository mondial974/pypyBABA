from dataclasses import dataclass
from math import sqrt, sin, cos
from pyEurocode5.pyEC5matbois import *
from pyEurocode2.utilsmath import interpolation
from pyEurocode2.utilsprint import *
import pandas as pd





@dataclass
class AssemblageBoisMetalBoulon:
    bois_1 : Bois
    bois_2 : Bois
    t_1 : float
    t_2 : float
    epaisseur_plaque : float
    classe_resistance_boulon : str
    reference_boulon : str
    mode_rupture : str
    alpha : float   
    F_ax_Rk : float


    # PLAQUE
    def type_plaque(self):
        if self.epaisseur_plaque <= 0.5 * self.diametre():
            return 'plaque mince'
        
        if self.epaisseur_plaque > 1.1 * self.diametre():
            return 'plaque épaisse'
        else:
            return 'plaque intermédiaire'
        
    
    
    # BOIS
    def f_h_0_k(self):
        d = self.diametre()
        rho_k = self.bois_1.rho_k()
        return 0.082 * (1. - 0.01 * d) * rho_k()
    
    def f_h_alpha_k_1(self):
        f_h_0_k = self.f_h_0_k_1()
        alpha = self.alpha
        k_90 = self.k_90_1()
        return f_h_0_k / (k_90 * (sin(alpha))**2. + (cos(alpha))**2.)
    
    def k_90_1(self):
        dict_k90 = {'résineux' : 1.35 * self.diametre(),
                    'LVL' : 1.30 * self.diametre(),
                    'feuillus' : 0.90 * self.diametre()}
        return dict_k90[self.bois.nature_bois]
    
    
    
    # BOULON
    def diametre(self):
        df = pd.read_excel(r"pyEurocode3/EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
        return df.at['d', self.reference_diametre]
      
    def f_yb(self):
        df = pd.read_excel(r"pyEurocode3/EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
        return df.at['f_yb', self.classe_resistance_organe]
    
    def f_ub(self):
        df = pd.read_excel(r"pyEurocode3/EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
        return df.at['f_ub', self.classe_resistance_organe]
    
    def M_y_Rk_boulon(self):
        return 0.3 * self.organe.f_ub() * pow(self.organe.diametre(), 2.6)
    
    def F_v_Rk_a(self):
        f_h_
        d = self.diametre()
        t1 = self.t1
        return 0.4 * fhk * t1 * d()
        
    def F_v_Rk_b(self):
        return 1.15 * sqrt(2 * MyRk * fhk * self.diametre()) + FaxRk / 4
    
    def F_v_Rk_c(self):
        return fhk * t1 * self.diametre()
            
    def F_v_Rk_d(self):
        return fhk * t1 * self.diametre() * (sqrt(2 + 4 * MyRk / (fhk * d * pow(t1, 2))) - 1) + FaRk / 4
    
    def F_v_Rk_e(self):
        return 2.3 * sqrt(MyRk * fhk * self.diametre())  + FaRk / 4
    
    def F_v_Rk_f(self):
        return fh1k * t1 * self.diametre()
    
    def F_v_Rk_g(self):
        return fh1k * t1 * self.diametre() * (sqrt(2 + 4 * MyRk / (fh1k * d * pow(t1, 2))) - 1) + FaRk / 4
    
    def F_v_Rk_h(self):
        return 2.3 * sqrt(MyRk * fh1k * d)  + FaRk / 4
    
    def F_v_Rk_j(self):
        return 0.5 * fh2k * t2 * d
        
    def F_v_Rk_k(self):
        return 1.15 * sqrt(2 * MyRk * fh2k * d) + FaxRk / 4
      
    def F_v_Rk_l(self):
        return 0.5 * fh2k * t2 * d
    
    def F_v_Rk_m(self):
        return 2.3 * sqrt(MyRk * fh2k * d)  + FaRk / 4
    
    def F_v_Rk_simple_cisaillement(self):
        FvRk_mince =  min(self.F_v_Rk_a(), self.F_v_Rk_b)
        FvRk_epaisse = min(self.F_v_Rk_c(), self.F_v_Rk_d(), self.F_v_Rk_e())
        
        if self.type_plaque() == 'plaque mince':
            return FvRk_mince
        
        if self.type_plaque() == 'plaque épaisse':
            return FvRk_epaisse
        
        if self.type_plaque() == 'plaque intermédiaire':
            x = self.epaisseur_plaque
            xa = 0.5 * self.diametre()
            xb = 1.1 * self.diametre()
            ya = FvRk_mince
            yb = FvRk_epaisse
            return interpolation(xa, xb, ya, yb, x)
 
        
    
    
    
    
    

