from dataclasses import dataclass
from math import sqrt, sin, cos
from pyEurocode2.utilsmath import interpolation
from pyEurocode2.utilsprint import *
import pandas as pd

@dataclass
class Profile:
    epaisseur : float
    classe_resistance_bois : str
    type_bois : str
    
    def f_m_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_m_g_k', self.classe_bois]
    
    def f_t_0_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_t_0_g_k', self.classe_bois]
    
    def f_t_90_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_t_90_g_k', self.classe_bois]
    
    def f_c_0_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_c_0_g_k', self.classe_bois]
    
    def f_c_90_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_c_90_g_k', self.classe_bois]
    
    def f_v_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_v_g_k', self.classe_bois]
    
    def f_r_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['f_r_g_k', self.classe_bois]
    
    def E_0_g_mean(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['E_0_g_mean', self.classe_bois]
    
    def E_0_g_05(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['E_0_g_05', self.classe_bois]
    
    def E_90_g_mean(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['E_90_g_mean', self.classe_bois]
    
    def E_90_g_05(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['E_90_g_05', self.classe_bois]
    
    def G_g_mean(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['G_g_mean', self.classe_bois]
    
    def G_g_05(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['G_g_05', self.classe_bois]
    
    def G_r_g_mean(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['G_r_g_mean', self.classe_bois]
    
    def G_r_g_05(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['G_r_g_05', self.classe_bois]
    
    def rho_g_k(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['E_90_g_05', self.classe_bois]
    
    def rho_g_mean(self):
        df = pd.read_excel(r"pyEurocode5/pyEC5_bdd_caracteristique_bois.xlsx", sheet='Lamellé_collé', index_col="Symbole")
        return df.at['rho_g_mean', self.classe_bois]
    
    def 
    
     
        
    
    
@dataclass
class Plaque:
    epaisseur : float
    organe : classmethod
        
    def diametre(self):
        return self.organe.diametre()
    
    def type_plaque(self):
        if self.epaisseur <= 0.5 * self.diametre():
            return 'plaque mince'
        
        if self.epaisseur > 1.1 * self.diametre():
            return 'plaque épaisse'
        else:
            return 'plaque intermédiaire'



@dataclass
class Boulon:
    organe : str = 'boulon'
    reference_diametre : str
    classe_resistance_organe : str
    
    def diametre(self):
        df = pd.read_excel(r"pyEurocode3/EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
        return df.at['d', self.reference_diametre]
      
    def f_yb(self):
        df = pd.read_excel(r"pyEurocode3/EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
        return df.at['f_yb', self.classe_resistance_organe]
    
    def f_ub(self):
        df = pd.read_excel(r"pyEurocode3/EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
        return df.at['f_ub', self.classe_resistance_organe]

        

@dataclass
class AssemblageBoisMetal:
    profile_1 : Profile
    profile_2 : Profile
    plaque : Plaque
    organe : Boulon
    mode_cisaillement : str
    
          
    def F_v_Rk_a(self):
        return 0.4 * fhk * t1 * d
        
    def F_v_Rk_b(self):
        return 1.15 * sqrt(2 * MyRk * fhk * d) + FaxRk / 4
    
    def F_v_Rk_c(self):
        return fhk * t1 * d
            
    def F_v_Rk_d(self):
        return fhk * t1 * d * (sqrt(2 + 4 * MyRk / (fhk * d * pow(t1, 2))) - 1) + FaRk / 4
    
    def F_v_Rk_e(self):
        return 2.3 * sqrt(MyRk * fhk * d)  + FaRk / 4
    
    def F_v_Rk_f(self):
        return fh1k * t1 * d
    
    def F_v_Rk_g(self):
        return fh1k * t1 * d * (sqrt(2 + 4 * MyRk / (fh1k * d * pow(t1, 2))) - 1) + FaRk / 4
    
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
        
        if self.plaque.type_plaque() == 'plaque mince':
            return FvRk_mince
        
        if self.plaque.type_plaque() == 'plaque épaisse':
            return FvRk_epaisse
        
        if self.plaque.type_plaque() == 'plaque intermédiaire':
            x = self.plaque.epaisseur
            xa = 0.5 * self.plaque.diametre_percage
            xb = 1.1 * self.plaque.diametre_percage
            ya = FvRk_mince
            yb = FvRk_epaisse
            return interpolation(xa, xb, ya, yb, x)
    
    def M_y_Rk(self):
        if self.organe.organe == 'boulon':
            return self.M_y_Rk_boulon()    
        
    
    # BOULONS
    def M_y_Rk_boulon(self):
        return 0.3 * self.organe.f_ub() * pow(self.organe.diametre(), 2.6)
    
    def f_h_0_k(self):
        return 0.082 * (1 - 0.01 * self.organe.diametre()) * self.profile_1.rho_g_k()
    
    def f_h_alpha_k(self):
        
        return self.f_h_0_k() / (self.k90() * pow(sin(alpha), 2) + pow(cos(alpha), 2))
    
    def k90(self):
        dict_k90 = {'résineux' : 1.35 * self.organe.diametre(),
                    'LVL' : 1.30 * self.organe.diametre(),
                    'feuillus' : 0.90 * self.organe.diametre()}
        return dict_k90[self.profile_1.type_bois]
    
    
    
    
    
    
    

